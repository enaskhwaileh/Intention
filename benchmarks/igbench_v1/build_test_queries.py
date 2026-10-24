"""IGBench-v1 held-out TEST queries.

Authored after the system design was frozen (IL 1.0.0, Profiler 3.0.0, Aligner 1.0) on topics
not used during development, and labelled from table documentation before any system was run
on them. Same label scale and status as the development set (draft, unreviewed).
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from build_queries import OWID, R, labels, q  # noqa: E402

CARS_MPG_CYL = [R + x for x in ["datasets.mtcars", "ISLR.Auto", "ggplot2.mpg", "MASS.Cars93", "openintro.cars04"]]
CARS_OTHER = [R + x for x in ["causaldata.auto", "usdatasets.Cars93_df", "DAAG.carprice", "gt.gtcars", "openintro.prius_mpg", "rpart.car90",
                              "rpart.car.test.frame", "rpart.cu.summary", "ipsRdbs.gasmileage", "Stat2Data.PorschePrice", "Stat2Data.PorscheJaguar",
                              "Stat2Data.ThreeCars", "Stat2Data.ThreeCars2017", "modeldata.car_prices", "datasets.cars"]]
USED_CAR_PRICE = [R + x for x in ["Stat2Data.PorschePrice", "Stat2Data.PorscheJaguar", "Stat2Data.ThreeCars", "Stat2Data.ThreeCars2017", "modeldata.car_prices"]]
BIRTHWT = [R + "MASS.birthwt", R + "MedDataSets.birthwt_df", R + "COUNT.lbw"]
BIRTHS_NC = [R + x for x in ["openintro.births14", "usdatasets.births14_tbl_df", "openintro.ncbirths", "usdatasets.ncbirths_tbl_df"]]
BIRTH_OTHER = [R + x for x in ["openintro.births", "usdatasets.births_tbl_df", "Stat2Data.NCbirths", "wooldridge.bwght2", "COUNT.lbwgrp", "mosaicData.Gestation"]]
US_BIRTH_COUNTS = [R + x for x in ["mosaicData.Births", "mosaicData.Births2015", "mosaicData.Births78", "mosaicData.BirthsCDC", "mosaicData.BirthsSSA", "openintro.present"]]
BIRTH_COUNT_OTHER = [R + x for x in ["openintro.arbuthnot", "HistData.Arbuthnot", "fpp3.aus_births"]]
GAPMINDER = [R + "gapminder.gapminder", R + "causaldata.gapminder", R + "gapminder.gapminder_unfiltered"]
LIFE_OTHER = [R + "dslabs.gapminder", R + "openintro.life_exp", R + "openintro.sowc_maternal_newborn", OWID["country_profile_latest"], OWID["country_weekly_panel"]]
US_CRIME_NATIONAL = [R + "crimedatasets.UScrimerates_tbl_df", R + "usdatasets.us_crime_rates_spec_tbl_df"]
CRIME_OTHER = [R + x for x in ["AER.Guns", "carData.Hartnagel", "crimedatasets.Hartnagel_df", "crimedatasets.Abilene_tbl_df", "causaldata.castle",
                               "wooldridge.countymurders", "crimedatasets.crimestatewide_tbl_df", "stevedata.af_crime93", "datasets.USArrests",
                               "crimedatasets.USArrests_df", "usdatasets.USArrests_df", "crimedatasets.crimeHSdegree_tbl_df",
                               "educationR.crime_degree_tbl_df", "crimedatasets.hate_crimes_tbl_df", "MASS.UScrime", "Ecdat.Crime"]]
STATE_MURDER = [R + x for x in ["datasets.USArrests", "crimedatasets.USArrests_df", "usdatasets.USArrests_df",
                                "crimedatasets.crimestatewide_tbl_df", "stevedata.af_crime93", "AER.Guns"]]
UNEMP = [R + x for x in ["openintro.unempl", "openintro.unemploy_pres", "openintro.midterms_house", "fpp3.us_change", "fpp2.uschange", "AER.GermanUnemployment"]]
HEART = [R + "CardioDataSets.heartdisease_tbl_df", R + "MLDataR.heartdisease"]
HEART_OTHER = [R + x for x in ["CardioDataSets.cardiac_failure_df", "CardioDataSets.heartdiseaserisk_tbl_df", "CardioDataSets.heartfailure_df",
                               "vcdExtra.Heart", "vcdExtra.Reinis"]]

T = []
T.append(q("T-CAR1", "cars", "Compare the average miles per gallon of cars by number of cylinders",
           expression="Compare", context="miles per gallon of cars by number of cylinders",
           args=[("statistic", "average"), ("measure", "miles per gallon of cars"), ("group_dimension", "number of cylinders")],
           variant="compare.group_means", bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=CARS_MPG_CYL, one=CARS_OTHER)))
T.append(q("T-CAR2", "cars", "Predict a car's fuel efficiency in miles per gallon from its weight and horsepower",
           expression="Predict", context="car fuel efficiency in miles per gallon, weight and horsepower",
           args=[("target", "fuel efficiency in miles per gallon"), ("predictor", "weight"), ("predictor", "horsepower")],
           variant="predict.regression", bindings={"target": ["a1"], "predictor": ["a2", "a3"]},
           labels_=labels(two=[R + x for x in ["datasets.mtcars", "ISLR.Auto", "MASS.Cars93", "openintro.cars04"]], one=CARS_MPG_CYL + CARS_OTHER)))
T.append(q("T-CAR3", "cars", "Is a used car's price associated with its mileage?",
           expression="associated with", context="used car price and mileage",
           args=[("measure", "used car's price"), ("predictor", "mileage")],
           variant="explain.association", bindings={"measure": ["a1"], "predictor": ["a2"]},
           labels_=labels(two=USED_CAR_PRICE, one=CARS_MPG_CYL + CARS_OTHER,
                          notes={R + "rpart.car.test.frame": "Mileage is fuel economy, not odometer reading"})))
T.append(q("T-CAR4", "cars", "Compare car prices", expression="Compare", context="car prices",
           args=[("measure", "car prices")], status="insufficient", family="compare",
           diagnostics=[{"code": "MISSING_ROLE", "role": "group_dimension", "entry_refs": []}],
           labels_=labels(one=CARS_OTHER + CARS_MPG_CYL)))
T.append(q("T-BW1", "births", "Predict whether a baby has low birth weight from the mother's age, smoking status and weight",
           expression="Predict", context="baby low birth weight, mother age, smoking status and weight",
           args=[("target", "has low birth weight"), ("predictor", "mother's age"), ("predictor", "smoking status"), ("predictor", "weight")],
           variant="predict.classification", bindings={"target": ["a1"], "predictor": ["a2", "a3", "a4"]},
           labels_=labels(two=BIRTHWT + BIRTHS_NC + [R + "wooldridge.bwght2"], one=BIRTH_OTHER + US_BIRTH_COUNTS)))
T.append(q("T-BW2", "births", "Compare the average birth weight of babies by mother's smoking status",
           expression="Compare", context="birth weight of babies by mother's smoking status",
           args=[("statistic", "average"), ("measure", "birth weight of babies"), ("group_dimension", "mother's smoking status")],
           variant="compare.group_means", bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=BIRTHWT + BIRTHS_NC + [R + x for x in ["openintro.births", "usdatasets.births_tbl_df", "Stat2Data.NCbirths", "mosaicData.Gestation"]],
                          one=BIRTH_OTHER, notes={R + "wooldridge.bwght2": "cigarettes per day, not a status", R + "COUNT.lbwgrp": "grouped counts"})))
T.append(q("T-BW3", "births", "How has the number of births in the United States changed over time?",
           expression="changed over time", context="number of births in the United States",
           args=[("measure", "number of births"), ("time_dimension", "over time")],
           scope=[("geography", "United States", "in the United States")], variant="monitor.trend",
           bindings={"measure": ["a1"], "time_dimension": ["a2"]},
           labels_=labels(two=US_BIRTH_COUNTS, one=BIRTH_COUNT_OTHER + BIRTHS_NC)))
T.append(q("T-LE1", "life-expectancy", "Compare the average life expectancy across continents in 2007",
           expression="Compare", context="life expectancy across continents in 2007",
           args=[("statistic", "average"), ("measure", "life expectancy"), ("group_dimension", "continents")],
           scope=[("period", "2007", "in 2007")], variant="compare.group_means",
           bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=GAPMINDER + [R + "dslabs.gapminder"], one=LIFE_OTHER)))
T.append(q("T-LE2", "life-expectancy", "Track life expectancy in Japan over time",
           expression="Track", context="life expectancy in Japan",
           args=[("measure", "life expectancy"), ("time_dimension", "over time")],
           scope=[("geography", "Japan", "in Japan")], variant="monitor.trend",
           bindings={"measure": ["a1"], "time_dimension": ["a2"]},
           labels_=labels(two=GAPMINDER + [R + "dslabs.gapminder"], one=LIFE_OTHER)))
T.append(q("T-LE3", "life-expectancy", "How is GDP per capita associated with life expectancy across countries?",
           expression="associated with", context="GDP per capita and life expectancy across countries",
           args=[("predictor", "GDP per capita"), ("measure", "life expectancy")],
           variant="explain.association", bindings={"measure": ["a2"], "predictor": ["a1"]},
           labels_=labels(two=GAPMINDER + [OWID["country_profile_latest"], OWID["country_weekly_panel"]], one=LIFE_OTHER,
                          notes={R + "dslabs.gapminder": "total GDP and population only"})))
T.append(q("T-LE4", "life-expectancy", "Gapminder life expectancy data", expression=None, context="Gapminder life expectancy data",
           status="not_attempted", labels_=labels(two=GAPMINDER + [R + "dslabs.gapminder"], one=LIFE_OTHER)))
T.append(q("T-CR1", "crime", "Track the number of violent crimes in the United States over time",
           expression="Track", context="number of violent crimes in the United States",
           args=[("measure", "number of violent crimes"), ("time_dimension", "over time")],
           scope=[("geography", "United States", "in the United States")], variant="monitor.trend",
           bindings={"measure": ["a1"], "time_dimension": ["a2"]},
           labels_=labels(two=US_CRIME_NATIONAL, one=CRIME_OTHER)))
T.append(q("T-CR2", "crime", "Compare the murder rates of California and Texas",
           expression="Compare", context="murder rates of California and Texas",
           args=[("measure", "murder rates"), ("groups", "California"), ("groups", "Texas")],
           variant="compare.observed_values", bindings={"measure": ["a1"], "groups": ["a2", "a3"]},
           labels_=labels(two=STATE_MURDER, one=CRIME_OTHER + US_CRIME_NATIONAL)))
T.append(q("T-CR3", "crime", "How is the share of people without a high school degree associated with violent crime across US states?",
           expression="associated with", context="share of people without a high school degree and violent crime across US states",
           args=[("predictor", "share of people without a high school degree"), ("measure", "violent crime")],
           variant="explain.association", bindings={"measure": ["a2"], "predictor": ["a1"]},
           labels_=labels(two=[R + "crimedatasets.crimeHSdegree_tbl_df", R + "educationR.crime_degree_tbl_df",
                               R + "crimedatasets.crimestatewide_tbl_df", R + "stevedata.af_crime93"], one=CRIME_OTHER + US_CRIME_NATIONAL)))
T.append(q("T-UN1", "unemployment", "Track the annual US unemployment rate since 1890",
           expression="Track", context="annual US unemployment rate since 1890",
           args=[("measure", "unemployment rate"), ("time_grain", "annual")],
           scope=[("period", "since 1890", "since 1890")], variant="monitor.trend",
           bindings={"measure": ["a1"], "time_grain": ["a2"]},
           labels_=labels(two=[R + "openintro.unempl"], one=UNEMP)))
T.append(q("T-EX1", "experiments", "Compare the average tooth length of guinea pigs across vitamin C doses",
           expression="Compare", context="tooth length of guinea pigs across vitamin C doses",
           args=[("statistic", "average"), ("measure", "tooth length of guinea pigs"), ("group_dimension", "vitamin C doses")],
           variant="compare.group_means", bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=[R + "datasets.ToothGrowth"])))
T.append(q("T-EX2", "experiments", "Compare the average plant weight across treatment groups",
           expression="Compare", context="plant weight across treatment groups",
           args=[("statistic", "average"), ("measure", "plant weight"), ("group_dimension", "treatment groups")],
           variant="compare.group_means", bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=[R + "datasets.PlantGrowth"], one=[R + "datasets.ChickWeight"])))
T.append(q("T-EX3", "experiments", "Track the body weight of chicks over time",
           expression="Track", context="body weight of chicks",
           args=[("measure", "body weight of chicks"), ("time_dimension", "over time")],
           variant="monitor.trend", bindings={"measure": ["a1"], "time_dimension": ["a2"]},
           labels_=labels(two=[R + "datasets.ChickWeight"], one=[R + "datasets.PlantGrowth"])))
T.append(q("T-IR1", "iris", "Predict the species of an iris flower from its petal and sepal measurements",
           expression="Predict", context="iris flower species, petal and sepal measurements",
           args=[("target", "species of an iris flower"), ("predictor", "petal and sepal measurements")],
           variant="predict.classification", bindings={"target": ["a1"], "predictor": ["a2"]},
           labels_=labels(two=[R + "datasets.iris"], one=[R + "datasets.iris3"], notes={R + "datasets.iris3": "species spread over columns"})))
T.append(q("T-HE1", "heart", "Predict whether a patient has heart disease from age, cholesterol and blood pressure",
           expression="Predict", context="patient heart disease, age, cholesterol and blood pressure",
           args=[("target", "has heart disease"), ("predictor", "age"), ("predictor", "cholesterol"), ("predictor", "blood pressure")],
           variant="predict.classification", bindings={"target": ["a1"], "predictor": ["a2", "a3", "a4"]},
           labels_=labels(two=HEART, one=HEART_OTHER, notes={t: "aggregated frequency table" for t in [R + "vcdExtra.Heart", R + "vcdExtra.Reinis"]})))
T.append(q("T-HE2", "heart", "Compare the average maximum heart rate by presence of heart disease",
           expression="Compare", context="maximum heart rate by presence of heart disease",
           args=[("statistic", "average"), ("measure", "maximum heart rate"), ("group_dimension", "presence of heart disease")],
           variant="compare.group_means", bindings={"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
           labels_=labels(two=HEART, one=HEART_OTHER)))


def main():
    from intention_grounding import corpus
    ids = {t["table_id"] for t in corpus.load_manifest()["tables"]}
    missing = sorted({t for item in T for t in item["labels"] if t not in ids})
    if missing:
        raise SystemExit("labelled tables not in corpus: " + ", ".join(missing))
    out = {"benchmark": "igbench-v1-test", "corpus_id": "igbench-v1", "label_scale": {"2": "useful", "1": "topical only", "0": "not relevant"},
           "label_status": "draft_author_labels_unreviewed", "default_label": 0,
           "protocol": "held-out: authored and labelled after design freeze (IL 1.0.0, Profiler 3.0.0, Aligner 1.0)", "queries": T}
    (HERE / "test_queries.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(len(T), "test queries;", sum(len(x["labels"]) for x in T), "judgements")


if __name__ == "__main__":
    main()
