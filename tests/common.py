"""Shared fixtures: a four-table corpus reproducing Figure 1 of the paper."""
import csv
import hashlib
import json
import tempfile
from pathlib import Path

FIG1 = Path(__file__).parent / "fixtures" / "fig1"

DOCS = {
    "regional_summary": ("Regional summary of COVID-19 vaccine side effects",
                         "Side-effect rates of COVID-19 vaccines per region and vaccine brand.",
                         {"region": "World region (continent)", "vaccine_brand": "Vaccine brand",
                          "mild_side_effect_rate": "Percentage of vaccinated people reporting mild side effects",
                          "severe_side_effect_rate": "Percentage of vaccinated people reporting severe side effects",
                          "observation_period": "Quarter of observation"}),
    "country_rates": ("COVID-19 vaccine side-effect rates by country",
                      "Mild and severe side-effect rates of COVID-19 vaccines by country, with vaccinated population.",
                      {"country": "Country", "vaccine_brand": "Vaccine brand",
                       "mild_side_effect_rate": "Percentage of vaccinated people reporting mild side effects",
                       "severe_side_effect_rate": "Percentage of vaccinated people reporting severe side effects",
                       "vaccinated_population": "Number of vaccinated people"}),
    "patient_records": ("COVID-19 vaccine patient records with observed side effects",
                        "One row per vaccinated patient: country, age, vaccine brand, dose, prior condition, observed side effect and severity.",
                        {"patient_id": "Patient identifier", "country": "Country of the patient", "age": "Age in years",
                         "vaccine_brand": "Vaccine brand", "dose": "Dose number", "prior_condition": "Prior medical condition",
                         "observed_side_effect": "Side effect type observed after vaccination",
                         "severity_score": "Severity score of the side effect (0-10)"}),
    "vaccine_logistics": ("COVID-19 vaccine logistics: shipments and storage",
                          "Vaccine shipments with doses delivered, storage temperature and delivery date.",
                          {"shipment_id": "Shipment identifier", "vaccine_brand": "Vaccine brand",
                           "doses_delivered": "Number of doses delivered", "storage_temperature": "Storage temperature in Celsius",
                           "delivery_date": "Date of delivery"}),
}


def fig1_manifest():
    tables = []
    for name, (title, description, cols) in DOCS.items():
        path = FIG1 / f"{name}.csv"
        with open(path, newline="") as f:
            header = next(csv.reader(f))
        tables.append({"table_id": f"fig1.{name}", "title": title, "description": description,
                       "path": str(path), "abs_path": str(path.resolve()),
                       "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size,
                       "source_family": "fig1", "columns": [{"name": c, "description": cols.get(c, "")} for c in header]})
    return {"corpus_id": "fig1-fixture", "tables": tables}


def tmpdir():
    return Path(tempfile.mkdtemp(prefix="ig-test-"))
