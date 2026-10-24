"""Build the IGBench table corpus from pinned public sources.

Sources (each pinned to a commit or hash and recorded in the manifest):
  owid       Our World in Data COVID-19 repository (CC BY 4.0), github.com/owid/covid-19-data
  uci        UCI Bike Sharing (275) and Seoul Bike Sharing Demand (560) (CC BY 4.0)
  rdatasets  Rdatasets collection (datasets shipped with CRAN packages), github.com/vincentarelbundock/Rdatasets

The corpus manifest is generic: any CSV collection described by
{table_id, title, description, path, columns:[{name, description}], ...}
can be used with the pipeline. Usage:

  python -m intention_grounding.corpus fetch      # git sparse/shallow clones into data/raw/
  python -m intention_grounding.corpus build      # writes data/corpus/igbench-v1/manifest.json
"""
import argparse
import csv
import hashlib
import html as html_lib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
CORPUS = ROOT / "data" / "corpus" / "igbench-v1"
GAZETTEER = Path(__file__).parent / "resources" / "gazetteer.json"

PINS = {
    "owid": {"url": "https://github.com/owid/covid-19-data", "commit": "dc00e7296b17ab5548092c9e388b6fac6751f095",
             "sparse": ["/public/data/vaccinations/", "/public/data/hospitalizations/", "/public/data/testing/covid-testing-all-observations.csv",
                        "/public/data/excess_mortality/", "/public/data/cases_deaths/full_data.csv", "/public/data/cases_deaths/new_cases.csv",
                        "/public/data/owid-covid-data.csv", "/public/data/owid-covid-codebook.csv", "/public/data/README.md"],
             "license": "CC BY 4.0"},
    "rdatasets": {"url": "https://github.com/vincentarelbundock/Rdatasets", "commit": "1dcc2bf5f955cc1224a3e1307256e1fe86b68dae",
                  "license": "Per originating CRAN package (mostly GPL-2/GPL-3); collection code GPL-3"},
}
RDATASETS_FILTER = {"max_rows": 100_000, "max_bytes": 5_000_000, "min_cols": 2}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _git(*args, cwd=None):
    subprocess.run(["git", *args], cwd=cwd, check=True)


def fetch(raw=RAW):
    """Shallow, sparse clones at the pinned commits (needs network and git)."""
    raw.mkdir(parents=True, exist_ok=True)
    owid = raw / "owid"
    if not owid.exists():
        _git("clone", "--filter=blob:none", "--no-checkout", "--sparse", PINS["owid"]["url"], str(owid))
        _git("sparse-checkout", "set", "--no-cone", *PINS["owid"]["sparse"], cwd=owid)
        _git("checkout", PINS["owid"]["commit"], cwd=owid)
    rd = raw / "rdatasets"
    if not rd.exists():
        _git("clone", "--filter=blob:none", "--no-checkout", PINS["rdatasets"]["url"], str(rd))
        _git("sparse-checkout", "set", "--no-cone", "/csv/", "/doc/", "/datasets.csv", cwd=rd)
        _git("checkout", PINS["rdatasets"]["commit"], cwd=rd)


# ----------------------------------------------------------------- documentation parsers
def readme_sections(text):
    """Map file name -> {column: description} from OWID README bullet lists."""
    sections, current = {}, None
    for line in text.splitlines():
        m = re.search(r"Stored in \[`([^`]+)`\]", line)
        if m:
            current = m.group(1)
            sections.setdefault(current, {})
            continue
        m = re.match(r"\s*[-*]\s+`([^`]+)`\s*:\s*(.+)", line)
        if m and current:
            sections[current][m.group(1)] = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", m.group(2)).strip()
    return sections


def markdown_table_docs(text):
    docs = {}
    for line in text.splitlines():
        m = re.match(r"\|\s*`([^`]+)`\s*\|\s*(.+?)\s*\|\s*$", line)
        if m:
            docs[m.group(1)] = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", m.group(2))
    return docs


def _strip(html_text):
    text = re.sub(r"<[^>]+>", " ", html_text)
    return re.sub(r"\s+", " ", html_lib.unescape(text)).strip()


def rdatasets_doc(path):
    """Description and variable documentation from an Rdatasets HTML help page."""
    if not path.exists():
        return "", {}
    text = path.read_text(encoding="utf-8", errors="replace")
    description = ""
    m = re.search(r"<h3>Description</h3>(.*?)<h3>", text, re.S)
    if m:
        description = _strip(m.group(1))
    columns = {}
    fmt = re.search(r"<h3>Format</h3>(.*?)(?:<h3>|$)", text, re.S)
    if fmt:
        block = fmt.group(1)
        for name, desc in re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", block, re.S):
            columns[_strip(name).strip("`'\"")] = _strip(desc)
        if not columns:
            for row in re.findall(r"<tr>(.*?)</tr>", block, re.S):
                cells = [_strip(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
                if len(cells) >= 2:
                    indexed = (cells[0].strip().isdigit() or re.fullmatch(r"\[\s*,\s*\d+\s*\]", cells[0].strip())) and len(cells) >= 3
                    name = cells[1] if indexed else cells[0]
                    desc = " ".join(cells[2:] if indexed else cells[1:])
                    if name and name.lower() not in ("name", "variable"):
                        columns[name.strip("`'\"")] = desc
        if fmt and not description:
            description = _strip(block)[:500]
    return description, columns


def uci_docs(readme):
    docs = {}
    for line in readme.splitlines():
        m = re.match(r"\s*-\s*([A-Za-z_]+)\s*:\s*(.+)", line)
        if m:
            docs[m.group(1).strip()] = m.group(2).strip()
    return docs


# ----------------------------------------------------------------- builders
def _table(table_id, title, description, path, columns_docs, *, source_family, source, license_, header=None,
           derivation=None, doc_source="source documentation"):
    path = Path(path)
    if header is None:
        with open(path, newline="", encoding="utf-8", errors="replace") as f:
            header = next(csv.reader(f))
    return {"table_id": table_id, "title": title, "description": description,
            "path": str(path.relative_to(ROOT)), "sha256": sha256(path), "bytes": path.stat().st_size,
            "source_family": source_family, "source": source, "license": license_,
            "derivation": derivation, "documentation_source": doc_source,
            "columns": [{"name": c, "description": columns_docs.get(c, "")} for c in header]}


def build_owid(raw=RAW, out=CORPUS):
    import pandas as pd
    base = raw / "owid" / "public" / "data"
    out_dir = out / "tables" / "owid"
    out_dir.mkdir(parents=True, exist_ok=True)
    vacc_readme = readme_sections((base / "vaccinations" / "README.md").read_text(encoding="utf-8"))
    codebook = {r["column"]: r["description"] for r in csv.DictReader(open(base / "owid-covid-codebook.csv", encoding="utf-8"))}
    excess_docs = readme_sections((base / "excess_mortality" / "README.md").read_text(encoding="utf-8"))
    hosp_docs = markdown_table_docs((base / "hospitalizations" / "README.md").read_text(encoding="utf-8"))
    src = {"repository": PINS["owid"]["url"], "commit": PINS["owid"]["commit"]}
    lic = PINS["owid"]["license"]
    tables = []

    def copy(name, rel, title, description, docs, **kw):
        target = out_dir / f"{name}.csv"
        df = pd.read_csv(base / rel, low_memory=False)
        df.to_csv(target, index=False, lineterminator="\n")
        tables.append(_table(f"owid.{name}", title, description, target, docs, source_family="owid-covid",
                             source={**src, "file": rel}, license_=lic, header=list(df.columns), **kw))
        return df

    agg_note = ("Includes subnational locations and international aggregates (World, continents, income groups); "
                "aggregates have iso codes starting with OWID_.")
    copy("vaccinations", "vaccinations/vaccinations.csv", "COVID-19 vaccinations by country and date",
         "Country-by-country daily data on global COVID-19 vaccinations from official public sources, collected by Our World in Data. " + agg_note,
         vacc_readme.get("vaccinations.csv", {}))
    age = vacc_readme.get("vaccinations-by-age-group.csv", {})
    copy("vaccinations_by_age_group", "vaccinations/vaccinations-by-age-group.csv",
         "COVID-19 vaccination coverage by age group, country and date",
         "Share of each age group that received at least one dose, completed the initial protocol, or received a booster, by country and date. Values are percentages of the age group's population.",
         age or {"location": "name of the country", "date": "date of the observation", "age_group": "age group of the population",
                 "people_vaccinated_per_hundred": "percentage of people in the age group who received at least one dose",
                 "people_fully_vaccinated_per_hundred": "percentage of people in the age group who completed the initial protocol",
                 "people_with_booster_per_hundred": "percentage of people in the age group who received a booster dose"})
    manu = vacc_readme.get("vaccinations-by-manufacturer.csv", {})
    copy("vaccinations_by_manufacturer", "vaccinations/vaccinations-by-manufacturer.csv",
         "COVID-19 vaccine doses administered by manufacturer, country and date",
         "Cumulative number of doses administered for each vaccine manufacturer, by country and date.",
         manu or {"location": "name of the country", "date": "date of the observation", "vaccine": "vaccine manufacturer",
                  "total_vaccinations": "cumulative number of doses administered of the vaccine up to the date"})
    copy("us_state_vaccinations", "vaccinations/us_state_vaccinations.csv",
         "COVID-19 vaccinations by United States state and date",
         "State-by-state data on United States COVID-19 vaccinations, from the US Centers for Disease Control and Prevention.",
         vacc_readme.get("us_state_vaccinations.csv", {}))
    copy("hospitalizations", "hospitalizations/covid-hospitalizations.csv",
         "COVID-19 hospital and ICU occupancy and admissions by country and date",
         "Hospital and intensive care occupancy and weekly admissions of COVID-19 patients, by country and date, in long format: one indicator per row. Indicators: daily hospital occupancy, daily ICU occupancy, weekly new hospital admissions, weekly new ICU admissions, each also per million people.",
         {**hosp_docs, "indicator": hosp_docs.get("indicator", "Indicator name") + ". One of: " + "; ".join(k for k in hosp_docs if k[0].isupper())})
    copy("testing", "testing/covid-testing-all-observations.csv",
         "COVID-19 testing observations by country and date",
         "Number of COVID-19 tests performed or people tested, by country and date, with source labels, cumulative totals, daily changes, per-thousand rates and short-term positive rates.",
         {"Entity": "country and testing unit (tests performed or people tested)", "ISO code": "ISO 3166-1 alpha-3 country code",
          "Date": "date of observation", "Cumulative total": "cumulative number of tests", "Daily change in cumulative total": "number of new tests on the day",
          "Cumulative total per thousand": "cumulative tests per 1,000 people", "Daily change in cumulative total per thousand": "new tests per 1,000 people",
          "7-day smoothed daily change": "new tests per day, 7-day rolling average", "7-day smoothed daily change per thousand": "new tests per 1,000 people, 7-day rolling average",
          "Short-term positive rate": "share of tests that are positive, 7-day rolling average", "Short-term tests per case": "tests conducted per new confirmed case, 7-day rolling average",
          "Source URL": "source web location", "Source label": "name of the source", "Notes": "notes"},
         doc_source="column names and OWID testing documentation (paraphrased)")
    copy("excess_mortality", "excess_mortality/excess_mortality.csv",
         "Excess mortality during the COVID-19 pandemic by country (weekly or monthly)",
         "Reported all-cause deaths, projected deaths and excess deaths (counts, per million and P-scores, by age band) by country and reporting week or month, from the Human Mortality Database and World Mortality Dataset.",
         excess_docs.get("excess_mortality.csv", {}))
    copy("cases_deaths", "cases_deaths/full_data.csv", "COVID-19 confirmed cases and deaths by country and date",
         "Daily new and cumulative confirmed COVID-19 cases and deaths reported to the WHO, by location and date. " + agg_note,
         {**{k: v for k, v in codebook.items()}, "location": "Geographical location", "date": "Date of observation",
          "weekly_cases": "New confirmed cases of COVID-19 in the last 7 days", "weekly_deaths": "New deaths attributed to COVID-19 in the last 7 days",
          "biweekly_cases": "New confirmed cases of COVID-19 in the last 14 days", "biweekly_deaths": "New deaths attributed to COVID-19 in the last 14 days"})
    wide = pd.read_csv(base / "cases_deaths" / "new_cases.csv")
    target = out_dir / "new_cases_wide.csv"
    wide.to_csv(target, index=False, lineterminator="\n")
    tables.append(_table("owid.new_cases_wide", "Daily new COVID-19 cases, one column per location",
                         "Daily new confirmed COVID-19 cases in wide format: one row per date and one column per country or aggregate region.",
                         target, {"date": "Date of observation", **{c: f"New confirmed cases of COVID-19 in {c}" for c in wide.columns if c != "date"}},
                         source_family="owid-covid", source={**src, "file": "cases_deaths/new_cases.csv"}, license_=lic, header=list(wide.columns)))
    master = pd.read_csv(base / "owid-covid-data.csv", low_memory=False, parse_dates=["date"])
    keep = ["location", "continent", "population", "median_age", "aged_65_older", "gdp_per_capita", "life_expectancy",
            "human_development_index", "hospital_beds_per_thousand", "people_vaccinated_per_hundred", "people_fully_vaccinated_per_hundred",
            "total_boosters_per_hundred", "total_cases_per_million", "total_deaths_per_million", "excess_mortality_cumulative_per_million"]
    latest = master.sort_values("date").groupby("location").agg({c: "last" for c in keep[1:]}).reset_index()
    iso = master.groupby("location")["iso_code"].first()
    latest["iso_code"] = latest["location"].map(iso)
    docs = {c: codebook.get(c, "") + (" Latest available value." if c.endswith(("hundred", "million")) else "") for c in keep}
    countries = latest[~latest["iso_code"].astype(str).str.startswith("OWID_")][keep]
    target = out_dir / "country_profile_latest.csv"
    countries.to_csv(target, index=False, lineterminator="\n")
    tables.append(_table("owid.country_profile_latest", "COVID-19 country profile: latest vaccination, cases and deaths rates with demographics",
                         "One row per country with continent, population, demographic indicators and the latest available COVID-19 vaccination, case and death rates.",
                         target, docs, source_family="owid-covid", source={**src, "file": "owid-covid-data.csv"}, license_=lic,
                         derivation="Latest non-missing value per country of selected owid-covid-data.csv columns; aggregate regions removed."))
    regions = latest[latest["location"].isin(["Africa", "Asia", "Europe", "North America", "Oceania", "South America", "World", "European Union (27)"])]
    rkeep = ["location", "population", "people_vaccinated_per_hundred", "people_fully_vaccinated_per_hundred", "total_boosters_per_hundred",
             "total_cases_per_million", "total_deaths_per_million"]
    target = out_dir / "regional_summary_latest.csv"
    regions[rkeep].to_csv(target, index=False, lineterminator="\n")
    rdocs = {c: docs.get(c, "") for c in rkeep}
    rdocs["location"] = "Continent or international aggregate region"
    tables.append(_table("owid.regional_summary_latest", "COVID-19 regional summary: latest vaccination, cases and deaths rates by continent",
                         "One row per continent or aggregate region (Africa, Asia, Europe, North America, Oceania, South America, European Union, World) with population and latest COVID-19 vaccination, case and death rates for the region as a whole.",
                         target, rdocs, source_family="owid-covid", source={**src, "file": "owid-covid-data.csv"}, license_=lic,
                         derivation="Latest non-missing value per aggregate region of owid-covid-data.csv."))
    weekly = master[(master["date"].dt.dayofweek == 6) & ~master["iso_code"].astype(str).str.startswith("OWID_")].copy()
    weekly["date"] = weekly["date"].dt.strftime("%Y-%m-%d")
    target = out_dir / "country_weekly_panel.csv"
    weekly.to_csv(target, index=False, lineterminator="\n")
    tables.append(_table("owid.country_weekly_panel", "COVID-19 weekly country panel: cases, deaths, hospitalizations, testing, vaccinations and demographics",
                         "Weekly snapshot (Sundays) per country of the complete Our World in Data COVID-19 dataset: confirmed cases and deaths, hospital and ICU figures, testing, vaccinations, policy stringency, excess mortality and demographic indicators. Aggregate regions removed.",
                         target, codebook, source_family="owid-covid", source={**src, "file": "owid-covid-data.csv"}, license_=lic,
                         header=list(weekly.columns), derivation="Rows of owid-covid-data.csv dated on Sundays for countries (iso codes not starting with OWID_)."))
    # Gazetteer: a declared membership mapping (country -> continent) with provenance.
    gaz = master[~master["iso_code"].astype(str).str.startswith("OWID_")].groupby("location")["continent"].first().dropna()
    states = sorted(pd.read_csv(base / "vaccinations" / "us_state_vaccinations.csv")["location"].unique())
    GAZETTEER.parent.mkdir(parents=True, exist_ok=True)
    GAZETTEER.write_text(json.dumps({"provenance": {**src, "file": "owid-covid-data.csv", "rule": "location -> continent for non-aggregate iso codes"},
                                     "country_continent": dict(sorted(gaz.items())),
                                     "continents": ["Africa", "Asia", "Europe", "North America", "Oceania", "South America", "Antarctica"],
                                     "aggregates": ["World", "European Union (27)", "European Union", "High-income countries", "Low-income countries",
                                                    "Lower-middle-income countries", "Upper-middle-income countries", "International"],
                                     "us_states": [s for s in states if s != "United States"]}, indent=1, ensure_ascii=False))
    return tables


def build_uci(root=ROOT):
    manifest = json.loads((root / "data" / "manifests" / "uci-bikes-v1.json").read_text())
    readme = (root / "data" / "raw" / "uci-275-Readme.txt").read_text(encoding="utf-8", errors="replace")
    docs275 = uci_docs(readme)
    seoul = {"Date": "day of observation", "Rented Bike Count": "count of bikes rented at each hour", "Hour": "hour of the day",
             "Temperature(°C)": "temperature in Celsius", "Humidity(%)": "relative humidity in percent", "Wind speed (m/s)": "wind speed",
             "Visibility (10m)": "visibility", "Dew point temperature(°C)": "dew point temperature", "Solar Radiation (MJ/m2)": "solar radiation",
             "Rainfall(mm)": "rainfall in mm", "Snowfall (cm)": "snowfall in cm", "Seasons": "season: Winter, Spring, Summer, Autumn",
             "Holiday": "Holiday or No holiday", "Functioning Day": "whether the rental system was functioning (Yes/No)"}
    tables = []
    for t in manifest["tables"]:
        path = root / t["path"]
        docs = docs275 if t["table_id"].startswith("uci-275") else seoul
        tables.append(_table("uci." + t["table_id"].replace("uci-", ""), t["title"] if t.get("title") and "Seoul" not in t["table_id"] else t.get("title", ""),
                             t["description"], path, docs, source_family="uci-bikes", source={"url": t["source_url"]},
                             license_=t["license"]))
    titles = {"uci.275-day": "Capital Bikeshare daily bike rental counts, Washington DC, 2011-2012 (UCI Bike Sharing Dataset, day.csv)",
              "uci.275-hour": "Capital Bikeshare hourly bike rental counts, Washington DC, 2011-2012 (UCI Bike Sharing Dataset, hour.csv)",
              "uci.560-hour": "Seoul Bike Sharing hourly rental demand with weather, 2017-2018 (UCI Seoul Bike Sharing Demand)"}
    for t in tables:
        t["title"] = titles.get(t["table_id"], t["title"])
    return tables


def build_rdatasets(raw=RAW, *, flt=RDATASETS_FILTER):
    base = raw / "rdatasets"
    rows = list(csv.DictReader(open(base / "datasets.csv", encoding="utf-8")))
    tables = []
    for r in rows:
        path = base / "csv" / r["Package"] / f"{r['Item']}.csv"
        if not path.exists():
            continue
        numeric = int(r["n_numeric"] or 0) + int(r["n_binary"] or 0)
        if int(r["Rows"]) > flt["max_rows"] or path.stat().st_size > flt["max_bytes"] or int(r["Cols"]) < flt["min_cols"] or numeric < 1:
            continue
        description, docs = rdatasets_doc(base / "doc" / r["Package"] / f"{r['Item']}.html")
        docs.setdefault("rownames", "Row identifier added by Rdatasets")
        tables.append(_table(f"rdatasets.{r['Package']}.{r['Item']}", r["Title"], description, path, docs,
                             source_family=f"rdatasets:{r['Package']}",
                             source={"repository": PINS["rdatasets"]["url"], "commit": PINS["rdatasets"]["commit"], "package": r["Package"], "item": r["Item"]},
                             license_=PINS["rdatasets"]["license"]))
    return tables


def build(out=CORPUS, *, include_rdatasets=True):
    tables = build_owid(out=out) + build_uci()
    if include_rdatasets:
        tables += build_rdatasets()
    ids = [t["table_id"] for t in tables]
    if len(ids) != len(set(ids)):
        raise ValueError("DUPLICATE_TABLE_ID")
    manifest = {"corpus_id": "igbench-v1", "created": datetime.now(timezone.utc).isoformat(),
                "pins": PINS, "rdatasets_filter": RDATASETS_FILTER, "table_count": len(tables),
                "source_families": sorted({t["source_family"].split(":")[0] for t in tables}), "tables": tables}
    out.mkdir(parents=True, exist_ok=True)
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    return manifest


def load_manifest(path=CORPUS / "manifest.json"):
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    for t in manifest["tables"]:
        t["abs_path"] = str((ROOT / t["path"]).resolve()) if not Path(t["path"]).is_absolute() else t["path"]
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["fetch", "build"])
    parser.add_argument("--no-rdatasets", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "fetch":
        fetch()
    else:
        m = build(include_rdatasets=not args.no_rdatasets)
        print(f"corpus {m['corpus_id']}: {m['table_count']} tables")


if __name__ == "__main__":
    main()
