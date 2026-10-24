"""Author IGBench-v1 queries, gold interpretations, gold groundings and draft usefulness labels.

Labels (graded, per query and table):
  2  useful: the table provides the data needed for the stated intention
  1  topical: about the requested subject, but cannot support the intention as stated
  0  not relevant (default for every unlisted table)
Status: DRAFT labels written by the framework author (assisted). They must be
independently reviewed before reporting effectiveness (see docs/EXPERIMENTS.md).
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
R = "rdatasets."

# ------------------------------------------------------------------ topic table groups
OWID = {k: f"owid.{k}" for k in ["vaccinations", "vaccinations_by_age_group", "vaccinations_by_manufacturer", "us_state_vaccinations",
                                  "hospitalizations", "testing", "excess_mortality", "cases_deaths", "new_cases_wide",
                                  "country_profile_latest", "regional_summary_latest", "country_weekly_panel"]}
TITANIC_PASSENGER = [R + "carData.TitanicSurvival", R + "causaldata.titanic", R + "COUNT.titanic", R + "Stat2Data.Titanic", R + "vcdExtra.Titanicp"]
TITANIC_AGG = [R + "datasets.Titanic", R + "COUNT.titanicgrp"]
TITANIC_OTHER = [R + "vcd.Lifeboats"]
WAGE_HOURLY_GENDER = [R + x for x in ["AER.CPS1985", "mosaicData.CPS85", "Ecdat.Bwages", "carData.SLID", "np.wage1", "AER.CPSSW04", "AER.CPSSW3",
                                      "AER.CPSSW8", "AER.CPSSW9204", "AER.CPSSW9298", "AER.CPSSWEducation", "Ecdat.CPSch3", "Ecdat.Wages1"]]
WAGE_OTHER = [R + x for x in ["carData.Salaries", "AER.PSID1982", "AER.PSID7682", "plm.Wages", "Ecdat.Wages", "AER.BankWages", "ISLR.Wage", "AER.CPS1988",
                              "Ecdat.Males", "plm.Males", "wooldridge.wage2", "wooldridge.wagepan", "camerondata.incpanel", "DAAG.wages1833",
                              "HistData.Wheat", "Ecdat.Earnings", "AER.Parade2005", "wooldridge.prminwge", "stevedata.min_wage", "np.cps71",
                              "Ecdat.LaborSupply", "plm.LaborSupply", "HLMdiag.wages", "causaldata.close_college"]]
BIKES = {"day": "uci.275-day", "hour": "uci.275-hour", "seoul": "uci.560-hour", "bikes": R + "bayesrules.bikes",
         "users": R + "bayesrules.bike_users", "nyc": R + "tsibbledata.nyc_bikes"}
HOUSE_UNIT = [R + x for x in ["AER.HousePrices", "Ecdat.Housing", "wooldridge.hprice1", "modeldata.ames", "wooldridge.kielmc", "Stat2Data.RailsTrails"]]
HOUSE_TOWN = [R + x for x in ["MASS.Boston", "crimedatasets.Boston_df", "usdatasets.Boston_df", "wooldridge.hprice2"]]
HOUSE_OTHER = [R + x for x in ["DAAG.houseprices", "ggplot2.txhousing", "MASS.housing", "Ecdat.Hstarts"]]
PIMA = [R + x for x in ["MASS.Pima.te", "MASS.Pima.tr", "MASS.Pima.tr2", "MedDataSets.Pima_te_df", "MedDataSets.Pima_tr_df", "MedDataSets.Pima_tr2_df"]]
DIAB_OTHER = [R + x for x in ["heplots.Diabetes", "MLDataR.diabetes_data", "MLDataR.PreDiabetes", "openintro.diabetes2", "MedDataSets.diabetes2_tbl_df",
                              "survival.diabetic", "survival.retinopathy", "fpp2.a10", "timeSeriesDataSets.a10_ts"]]
AIRQ = [R + "datasets.airquality", R + "usdatasets.airquality_df"]
AIR_OTHER = [R + x for x in ["lattice.environmental", "robustbase.airmay", "Ecdat.Airq", "openintro.pm25_2011_durham", "openintro.pm25_2022_durham",
                             "DAAG.ozone", "texmex.summer", "texmex.winter"]]
COVID_OTHER = [R + x for x in ["MedDataSets.covid19sf_hospital_df", "MedDataSets.covid19sf_tests_df", "medicaldata.covid_testing",
                               "openintro.biontech_adolescents", "MedDataSets.biontech_teens_tbl_df"]]


def labels(two=(), one=(), notes=None):
    out = {t: 1 for t in one}
    out.update({t: 2 for t in two})
    return out, notes or {}


def entry(i, label, value, span=None, prefix="a"):
    return {"id": f"{prefix}{i}", "label": label, "value": value, "spans": [span or value]}


def q(qid, topic, text, *, expression, context, args=(), scope=(), variant=None, bindings=None, status="grounded",
      diagnostics=None, labels_=None, pair=None, family=None):
    z = {"context_query": context, "intention_expression": expression,
         "arguments": [entry(i + 1, *a) for i, a in enumerate(args)],
         "scope": [entry(i + 1, *s, prefix="s") for i, s in enumerate(scope)]}
    if status == "grounded":
        proposal = {"status": "proposed", "variant_id": variant, "bindings": bindings or {},
                    "scope": [s["id"] for s in z["scope"]], "justification": "gold", "diagnostics": []}
    elif status == "not_attempted":
        proposal = None
    else:
        proposal = {"status": status, "variant_id": None, "bindings": {}, "scope": [s["id"] for s in z["scope"]],
                    "justification": "gold", "diagnostics": diagnostics or []}
    lab, notes = labels_
    for text_ in [s for e in z["arguments"] + z["scope"] for s in e["spans"]] + ([expression] if expression else []):
        assert text_.casefold() in text.casefold(), (qid, text_)
    return {"query_id": qid, "topic": topic, "pair_group": pair or topic, "text": text,
            "gold_family": family or (variant.split(".")[0] if variant else None), "gold_variant": variant,
            "gold_grounding_status": status, "gold_interpretation": z, "gold_grounding": proposal,
            "labels": lab, "label_notes": notes}


Q = []
# ------------------------------------------------------------------ COVID-19 (Our World in Data + Rdatasets)
VACC_TOPICAL = [OWID[k] for k in ["vaccinations", "vaccinations_by_age_group", "vaccinations_by_manufacturer", "us_state_vaccinations",
                                  "country_profile_latest", "regional_summary_latest", "country_weekly_panel"]] + [R + "openintro.biontech_adolescents", R + "MedDataSets.biontech_teens_tbl_df"]
CASES_TOPICAL = [OWID[k] for k in ["cases_deaths", "new_cases_wide", "country_weekly_panel", "testing", "hospitalizations", "country_profile_latest",
                                   "regional_summary_latest"]] + [R + "MedDataSets.covid19sf_tests_df"]
Q.append(q("C1", "covid-vaccination", "Compare the share of people fully vaccinated against COVID-19 across countries in Europe",
           expression="Compare", context="share of people fully vaccinated against COVID-19 across countries in Europe",
           args=[("measure", "share of people fully vaccinated against COVID-19"), ("group_dimension", "countries")],
           scope=[("geography", "Europe", "in Europe")], variant="compare.observed_values",
           bindings={"measure": ["a1"], "group_dimension": ["a2"]},
           labels_=labels(two=[OWID["country_profile_latest"], OWID["vaccinations"], OWID["country_weekly_panel"]], one=VACC_TOPICAL,
                          notes={OWID["regional_summary_latest"]: "continent level only; country distinctions lost",
                                 OWID["vaccinations_by_age_group"]: "rates only within age groups",
                                 OWID["us_state_vaccinations"]: "United States states, not Europe"})))
Q.append(q("C2", "covid-cases", "Compare the average daily number of new COVID-19 cases across continents in 2021",
           expression="Compare", context="daily number of new COVID-19 cases across continents in 2021",
           args=[("statistic", "average"), ("measure", "daily number of new COVID-19 cases"), ("group_dimension", "continents")],
           scope=[("period", "2021", "in 2021")], variant="compare.group_means",
           bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=[OWID["cases_deaths"], OWID["new_cases_wide"]], one=CASES_TOPICAL,
                          notes={OWID["cases_deaths"]: "continent aggregate rows with daily new cases",
                                 OWID["new_cases_wide"]: "one daily column per continent",
                                 OWID["country_weekly_panel"]: "country rows only; a mean over countries is not the continent mean"})))
Q.append(q("C3", "covid-hospital", "How has COVID-19 hospital occupancy in France changed over time?",
           expression="changed over time", context="COVID-19 hospital occupancy in France",
           args=[("measure", "COVID-19 hospital occupancy"), ("time_dimension", "over time")],
           scope=[("geography", "France", "in France")], variant="monitor.trend",
           bindings={"measure": ["a1"], "time_dimension": ["a2"]},
           labels_=labels(two=[OWID["hospitalizations"], OWID["country_weekly_panel"]],
                          one=[OWID["cases_deaths"], R + "MedDataSets.covid19sf_hospital_df", OWID["country_profile_latest"]])))
Q.append(q("C4", "covid-vaccination", "What is the total number of COVID-19 vaccine doses administered by each manufacturer in Germany?",
           expression="total number", context="COVID-19 vaccine doses administered by each manufacturer in Germany",
           args=[("statistic", "total number"), ("measure", "COVID-19 vaccine doses administered"), ("group_dimension", "manufacturer")],
           scope=[("geography", "Germany", "in Germany")], variant="aggregate.group_totals",
           bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=[OWID["vaccinations_by_manufacturer"]], one=VACC_TOPICAL)))
Q.append(q("C5", "covid-vaccination", "Is the COVID-19 death rate per million associated with the share of people fully vaccinated?",
           expression="associated with", context="COVID-19 death rate per million and share of people fully vaccinated",
           args=[("measure", "COVID-19 death rate per million"), ("predictor", "share of people fully vaccinated")],
           variant="explain.association", bindings={"measure": ["a1"], "predictor": ["a2"]},
           labels_=labels(two=[OWID["country_profile_latest"], OWID["country_weekly_panel"]],
                          one=VACC_TOPICAL + [OWID["cases_deaths"], OWID["excess_mortality"]],
                          notes={OWID["regional_summary_latest"]: "eight aggregate rows: too few co-observations"})))
Q.append(q("C6", "covid-deaths", "Predict a country's COVID-19 deaths per million from its median age, GDP per capita and vaccination rate",
           expression="Predict", context="country COVID-19 deaths per million, median age, GDP per capita and vaccination rate",
           args=[("target", "COVID-19 deaths per million"), ("predictor", "median age"), ("predictor", "GDP per capita"), ("predictor", "vaccination rate")],
           variant="predict.regression", bindings={"target": ["a1"], "predictor": ["a2", "a3", "a4"]},
           labels_=labels(two=[OWID["country_profile_latest"], OWID["country_weekly_panel"]],
                          one=[OWID["regional_summary_latest"], OWID["cases_deaths"], OWID["excess_mortality"], OWID["vaccinations"]])))
Q.append(q("C7", "covid-vaccination", "Compare the number of people vaccinated in the United States on 2021-06-01 and 2022-06-01",
           expression="Compare", context="number of people vaccinated in the United States",
           args=[("measure", "number of people vaccinated"), ("time_points", "2021-06-01"), ("time_points", "2022-06-01")],
           scope=[("geography", "United States", "in the United States")], variant="compare.observed_values",
           bindings={"measure": ["a1"], "groups": ["a2", "a3"]},
           labels_=labels(two=[OWID["vaccinations"], OWID["us_state_vaccinations"]], one=VACC_TOPICAL,
                          notes={OWID["country_weekly_panel"]: "weekly Sunday snapshots: the requested dates are absent"})))
Q.append(q("C8", "covid-vaccination", "COVID-19 vaccination data for European countries",
           expression=None, context="COVID-19 vaccination data for European countries", status="not_attempted", family=None,
           labels_=labels(two=[OWID[k] for k in ["vaccinations", "vaccinations_by_age_group", "vaccinations_by_manufacturer",
                                                 "country_profile_latest", "country_weekly_panel"]],
                          one=VACC_TOPICAL)))
Q.append(q("C9", "covid-vaccination", "Compare COVID-19 vaccine side effects in Europe",
           expression="Compare", context="COVID-19 vaccine side effects in Europe",
           args=[("measure", "COVID-19 vaccine side effects")], scope=[("geography", "Europe", "in Europe")],
           status="insufficient", family="compare", diagnostics=[{"code": "MISSING_ROLE", "role": "group_dimension", "entry_refs": []}],
           labels_=labels(one=VACC_TOPICAL, notes={"*": "no table reports side effects: no useful table exists"})))
Q.append(q("C10", "covid-testing", "Predict whether a patient tests positive for COVID-19 from their age, gender and clinic",
           expression="Predict", context="patient COVID-19 test result, age, gender and clinic",
           args=[("target", "tests positive for COVID-19"), ("predictor", "age"), ("predictor", "gender"), ("predictor", "clinic")],
           variant="predict.classification", bindings={"target": ["a1"], "predictor": ["a2", "a3", "a4"]},
           labels_=labels(two=[R + "medicaldata.covid_testing"], one=[R + "MedDataSets.covid19sf_tests_df", OWID["testing"]])))

# ------------------------------------------------------------------ Titanic
ALL_TIT = TITANIC_PASSENGER + TITANIC_AGG + TITANIC_OTHER
Q.append(q("TI1", "titanic", "Predict whether a Titanic passenger survived from their class, sex and age",
           expression="Predict", context="Titanic passenger survival, class, sex and age",
           args=[("target", "survived"), ("predictor", "class"), ("predictor", "sex"), ("predictor", "age")],
           variant="predict.classification", bindings={"target": ["a1"], "predictor": ["a2", "a3", "a4"]},
           labels_=labels(two=TITANIC_PASSENGER, one=ALL_TIT, notes={t: "aggregated cells, not passenger rows" for t in TITANIC_AGG})))
Q.append(q("TI2", "titanic", "Compare the average survival rate of Titanic passengers across passenger classes",
           expression="Compare", context="survival rate of Titanic passengers across passenger classes",
           args=[("statistic", "average"), ("measure", "survival rate"), ("group_dimension", "passenger classes")],
           variant="compare.group_means", bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=TITANIC_PASSENGER, one=ALL_TIT, notes={t: "rate derivable only with weighted counts" for t in TITANIC_AGG})))
Q.append(q("TI3", "titanic", "How is passenger age associated with survival on the Titanic?",
           expression="associated with", context="Titanic passenger age and survival",
           args=[("predictor", "passenger age"), ("measure", "survival")],
           variant="explain.association", bindings={"measure": ["a2"], "predictor": ["a1"]},
           labels_=labels(two=[R + "carData.TitanicSurvival", R + "Stat2Data.Titanic", R + "vcdExtra.Titanicp"], one=ALL_TIT,
                          notes={R + "causaldata.titanic": "age only as child/adult", R + "COUNT.titanic": "age only as child/adult"})))
Q.append(q("TI4", "titanic", "How many Titanic passengers survived in each passenger class?",
           expression="How many", context="Titanic passengers survived in each passenger class",
           args=[("statistic", "How many"), ("measure", "passengers survived"), ("group_dimension", "passenger class")],
           variant="aggregate.group_totals", bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=TITANIC_PASSENGER + TITANIC_AGG, one=ALL_TIT)))

# ------------------------------------------------------------------ Wages
ALL_WAGE = WAGE_HOURLY_GENDER + WAGE_OTHER
Q.append(q("W1", "wages", "Compare the average hourly wage across genders",
           expression="Compare", context="hourly wage across genders",
           args=[("statistic", "average"), ("measure", "hourly wage"), ("group_dimension", "genders")],
           variant="compare.group_means", bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=WAGE_HOURLY_GENDER, one=ALL_WAGE)))
Q.append(q("W2", "wages", "Predict a worker's hourly wage from education, experience and gender",
           expression="Predict", context="worker hourly wage, education, experience and gender",
           args=[("target", "hourly wage"), ("predictor", "education"), ("predictor", "experience"), ("predictor", "gender")],
           variant="predict.regression", bindings={"target": ["a1"], "predictor": ["a2", "a3", "a4"]},
           labels_=labels(two=[R + x for x in ["AER.CPS1985", "mosaicData.CPS85", "Ecdat.Bwages", "np.wage1", "Ecdat.Wages1", "carData.SLID",
                                               "AER.CPSSW8", "AER.CPSSWEducation", "AER.CPSSW04", "AER.CPSSW9204", "AER.CPSSW9298"]], one=ALL_WAGE)))
Q.append(q("W3", "wages", "Is a worker's hourly wage associated with years of education?",
           expression="associated with", context="worker hourly wage and years of education",
           args=[("measure", "hourly wage"), ("predictor", "years of education")],
           variant="explain.association", bindings={"measure": ["a1"], "predictor": ["a2"]},
           labels_=labels(two=[R + x for x in ["AER.CPS1985", "mosaicData.CPS85", "Ecdat.Bwages", "np.wage1", "carData.SLID", "AER.CPSSW8",
                                               "AER.CPSSWEducation", "Ecdat.Wages1", "Ecdat.Males", "plm.Males"]], one=ALL_WAGE)))
Q.append(q("W4", "wages", "How have average hourly earnings changed over time?",
           expression="changed over time", context="average hourly earnings",
           args=[("measure", "average hourly earnings"), ("time_dimension", "over time")],
           variant="monitor.trend", bindings={"measure": ["a1"], "time_dimension": ["a2"]},
           labels_=labels(two=[R + x for x in ["AER.CPSSW3", "Ecdat.CPSch3", "AER.PSID7682", "Ecdat.Males", "plm.Males", "wooldridge.wagepan",
                                               "ISLR.Wage", "wooldridge.prminwge"]], one=ALL_WAGE,
                          notes={R + "AER.CPSSW9204": "two years only", R + "AER.CPSSW9298": "two years only"})))
Q.append(q("W5", "wages", "Compare the weekly wages of a good mechanic in 1700 and 1800",
           expression="Compare", context="weekly wages of a good mechanic",
           args=[("measure", "weekly wages"), ("time_points", "1700"), ("time_points", "1800"), ("subject", "good mechanic")],
           variant="compare.observed_values", bindings={"measure": ["a1"], "groups": ["a2", "a3"]},
           labels_=labels(two=[R + "HistData.Wheat"], one=ALL_WAGE)))

# ------------------------------------------------------------------ Bike sharing
ALL_BIKE = list(BIKES.values())
Q.append(q("B1", "bikes", "Track daily bike rental counts in Washington DC over time",
           expression="Track", context="daily bike rental counts in Washington DC",
           args=[("measure", "bike rental counts"), ("time_grain", "daily"), ("time_dimension", "over time")],
           scope=[("geography", "Washington DC", "in Washington DC")], variant="monitor.trend",
           bindings={"measure": ["a1"], "time_grain": ["a2"], "time_dimension": ["a3"]},
           labels_=labels(two=[BIKES["day"], BIKES["bikes"]], one=ALL_BIKE,
                          notes={BIKES["hour"]: "hourly rows need summing per day", BIKES["users"]: "rides split by rider type"})))
Q.append(q("B2", "bikes", "Compare the average hourly bike rental count across seasons in Washington DC",
           expression="Compare", context="hourly bike rental count across seasons in Washington DC",
           args=[("statistic", "average"), ("measure", "hourly bike rental count"), ("group_dimension", "seasons")],
           scope=[("geography", "Washington DC", "in Washington DC")], variant="compare.group_means",
           bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=[BIKES["hour"]], one=ALL_BIKE, notes={BIKES["seoul"]: "Seoul, not Washington DC"})))
Q.append(q("B3", "bikes", "Predict the number of bike rentals per day from temperature, humidity and wind speed",
           expression="Predict", context="number of bike rentals per day, temperature, humidity and wind speed",
           args=[("target", "number of bike rentals per day"), ("predictor", "temperature"), ("predictor", "humidity"), ("predictor", "wind speed")],
           variant="predict.regression", bindings={"target": ["a1"], "predictor": ["a2", "a3", "a4"]},
           labels_=labels(two=[BIKES["day"], BIKES["bikes"]], one=ALL_BIKE)))
Q.append(q("B4", "bikes", "How does temperature affect the number of bike rentals?",
           expression="affect", context="temperature and number of bike rentals",
           args=[("predictor", "temperature"), ("measure", "number of bike rentals")],
           variant="explain.association", bindings={"measure": ["a2"], "predictor": ["a1"]},
           labels_=labels(two=[BIKES[k] for k in ["day", "hour", "seoul", "bikes", "users"]], one=ALL_BIKE)))
Q.append(q("B5", "bikes", "What was the total number of bike rentals per season in 2011 in Washington DC?",
           expression="total number", context="bike rentals per season in 2011 in Washington DC",
           args=[("statistic", "total number"), ("measure", "bike rentals"), ("group_dimension", "season")],
           scope=[("period", "2011", "in 2011"), ("geography", "Washington DC", "in Washington DC")], variant="aggregate.group_totals",
           bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=[BIKES["day"], BIKES["hour"]], one=ALL_BIKE, notes={BIKES["bikes"]: "500 sampled days: totals incomplete"})))

# ------------------------------------------------------------------ Housing
ALL_HOUSE = HOUSE_UNIT + HOUSE_TOWN + HOUSE_OTHER
Q.append(q("H1", "housing", "Predict the sale price of a house from its lot size, number of bedrooms and bathrooms",
           expression="Predict", context="house sale price, lot size, number of bedrooms and bathrooms",
           args=[("target", "sale price of a house"), ("predictor", "lot size"), ("predictor", "number of bedrooms"), ("predictor", "bathrooms")],
           variant="predict.regression", bindings={"target": ["a1"], "predictor": ["a2", "a3", "a4"]},
           labels_=labels(two=HOUSE_UNIT, one=ALL_HOUSE, notes={R + "DAAG.houseprices": "15 houses only"})))
Q.append(q("H2", "housing", "Compare the average sale price of houses by air conditioning",
           expression="Compare", context="sale price of houses by air conditioning",
           args=[("statistic", "average"), ("measure", "sale price of houses"), ("group_dimension", "air conditioning")],
           variant="compare.group_means", bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=[R + "AER.HousePrices", R + "Ecdat.Housing", R + "modeldata.ames"], one=ALL_HOUSE)))
Q.append(q("H3", "housing", "Track the median house sale price in Austin over time",
           expression="Track", context="median house sale price in Austin",
           args=[("measure", "median house sale price"), ("time_dimension", "over time")],
           scope=[("geography", "Austin", "in Austin")], variant="monitor.trend",
           bindings={"measure": ["a1"], "time_dimension": ["a2"]},
           labels_=labels(two=[R + "ggplot2.txhousing"], one=ALL_HOUSE)))
Q.append(q("H4", "housing", "How is the median home value of a town associated with its crime rate?",
           expression="associated with", context="town median home value and crime rate",
           args=[("measure", "median home value"), ("predictor", "crime rate")],
           variant="explain.association", bindings={"measure": ["a1"], "predictor": ["a2"]},
           labels_=labels(two=HOUSE_TOWN, one=ALL_HOUSE)))

# ------------------------------------------------------------------ Diabetes
ALL_DIAB = PIMA + DIAB_OTHER
Q.append(q("D1", "diabetes", "Predict whether a woman has diabetes from her glucose level, BMI and age",
           expression="Predict", context="woman diabetes, glucose level, BMI and age",
           args=[("target", "has diabetes"), ("predictor", "glucose level"), ("predictor", "BMI"), ("predictor", "age")],
           variant="predict.classification", bindings={"target": ["a1"], "predictor": ["a2", "a3", "a4"]},
           labels_=labels(two=PIMA, one=ALL_DIAB)))
Q.append(q("D2", "diabetes", "Compare the average plasma glucose concentration by diabetes status",
           expression="Compare", context="plasma glucose concentration by diabetes status",
           args=[("statistic", "average"), ("measure", "plasma glucose concentration"), ("group_dimension", "diabetes status")],
           variant="compare.group_means", bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=PIMA + [R + "heplots.Diabetes"], one=ALL_DIAB)))
Q.append(q("D3", "diabetes", "Is body mass index associated with diabetes?",
           expression="associated with", context="body mass index and diabetes",
           args=[("predictor", "body mass index"), ("measure", "diabetes")],
           variant="explain.association", bindings={"measure": ["a2"], "predictor": ["a1"]},
           labels_=labels(two=PIMA, one=ALL_DIAB)))

# ------------------------------------------------------------------ Air quality
ALL_AIR = AIRQ + AIR_OTHER
Q.append(q("A1", "air-quality", "How does temperature affect ozone concentration in New York?",
           expression="affect", context="temperature and ozone concentration in New York",
           args=[("predictor", "temperature"), ("measure", "ozone concentration")],
           scope=[("geography", "New York", "in New York")], variant="explain.association",
           bindings={"measure": ["a2"], "predictor": ["a1"]},
           labels_=labels(two=AIRQ + [R + "lattice.environmental", R + "robustbase.airmay"], one=ALL_AIR)))
Q.append(q("A2", "air-quality", "Track daily PM2.5 concentration in Durham over time",
           expression="Track", context="daily PM2.5 concentration in Durham",
           args=[("measure", "PM2.5 concentration"), ("time_grain", "daily"), ("time_dimension", "over time")],
           scope=[("geography", "Durham", "in Durham")], variant="monitor.trend",
           bindings={"measure": ["a1"], "time_grain": ["a2"], "time_dimension": ["a3"]},
           labels_=labels(two=[R + "openintro.pm25_2011_durham", R + "openintro.pm25_2022_durham"], one=ALL_AIR)))
Q.append(q("A3", "air-quality", "Predict ozone levels from solar radiation, wind speed and temperature",
           expression="Predict", context="ozone levels, solar radiation, wind speed and temperature",
           args=[("target", "ozone levels"), ("predictor", "solar radiation"), ("predictor", "wind speed"), ("predictor", "temperature")],
           variant="predict.regression", bindings={"target": ["a1"], "predictor": ["a2", "a3", "a4"]},
           labels_=labels(two=AIRQ + [R + "lattice.environmental", R + "robustbase.airmay"], one=ALL_AIR)))

# ------------------------------------------------------------------ no intention
Q.append(q("N1", "bikes", "Bike sharing rental data", expression=None, context="Bike sharing rental data", status="not_attempted",
           labels_=labels(two=[BIKES[k] for k in ["day", "hour", "seoul", "bikes", "users"]], one=ALL_BIKE)))
Q.append(q("N2", "housing", "House sale prices", expression=None, context="House sale prices", status="not_attempted",
           labels_=labels(two=HOUSE_UNIT + [R + "DAAG.houseprices"], one=ALL_HOUSE)))


def main():
    from intention_grounding import corpus
    manifest = corpus.load_manifest()
    ids = {t["table_id"] for t in manifest["tables"]}
    missing = sorted({t for item in Q for t in item["labels"] if t not in ids})
    if missing:
        raise SystemExit("labelled tables not in corpus: " + ", ".join(missing))
    out = {"benchmark": "igbench-v1", "corpus_id": manifest["corpus_id"], "label_scale": {"2": "useful", "1": "topical only", "0": "not relevant"},
           "label_status": "draft_author_labels_unreviewed", "default_label": 0, "queries": Q}
    (HERE / "queries.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(len(Q), "queries;", sum(len(x["labels"]) for x in Q), "judgements")


if __name__ == "__main__":
    main()
