from csv import DictReader
from functools import namedtuple
from argparse import ArgumentParser
from copy import deepcopy

parser = ArgumentParser()
parser.add_argument("--filename", "-if", type=str, help="Input file")
args = parser.parse_args()

info_data = namedtuple("info", "cid country iname years data")

def remove_headings(data: dict) -> dict:

    data.pop("ï»¿CountryID")
    data.pop("Country")
    data.pop("IndicatorName")
    
    return data

def parse_gdp(data: str) -> int:
	return int(data.replace(".", ""))

def parse_data(data_row: str) -> namedtuple:

    cid, country, iname = data_row["ï»¿CountryID"], data_row["Country"], data_row["IndicatorName"]
    years               = {k: parse_gdp(v) for k, v in remove_headings(data_row).items() if v != ""}
    data                = list(filter(None, [years[year] for year in years.keys()]))

    return info_data(cid, country, iname, years, data)

def count(row):

    c = 0
    for year, num in row.items():
        if not num:
            c += 1

    return c

def task_411_a(data, iname: str):
    ret = []

    for row in data:

        if row["IndicatorName"] == iname:
            c      = count(row)
            result = 50 - c

            ret.append(
                (row["Country"], result)
            )

    return ret

def task_411_b(data):

    cc = 0

    for row in data:
        
        if row["IndicatorName"] == "Final consumption expenditure":

            c   = count(row)
            res = 50 - c

            if res == 50:
                cc += 1

    percentage = round(((220 - cc) * 100) / 220, 2)

    return cc, percentage

def task_411_2(data, *countries, force_country_limit=False):

    def ignore_headings(data: dict) -> dict:
        return {k: v for k, v in data.items() if k != "ï»¿CountryID" and k != "Country" and k != "IndicatorName"}

    if force_country_limit and len(countries) != 3:
        raise ValueError("You must provide 3 countries")

    all_exports = []
    all_imports = []

    for row in data:
        for country in countries:

            if row["Country"] == country and row["IndicatorName"] == "Exports of goods and services":
                exports = ignore_headings(row)
                all_exports.append((country, exports))
            elif row["Country"] == country and row["IndicatorName"] == "Imports of goods and services":
                imports = ignore_headings(row)
                all_imports.append((country, imports))

    net_exports = []
    for exports, imports in zip(all_exports, all_imports):

        country = exports[0]
        ret     = []

        for x, y in zip(exports[1].values(), imports[1].values()):
            x = int(x.replace(".", ""))
            y = int(y.replace(".", ""))
            ret.append(x - y)

        net_exports.append(
            (country, {str(i): v for i, v in enumerate(ret, 1970)})
        )

    return net_exports

    #ret      = [(sd(x) - sd(y)) for e, i in zip(all_exports, all_imports) for x, y in zip(e[1].values(), i[1].values()) if (sd := lambda x: int(x.replace(".", "")))]
    #splitted = [ret[i: i + 50] for i in range(0, len(ret), 50)]
    #print(splitted)

def main(filename: str):
    
    with open(filename, newline='') as csvdata:
        reader = DictReader(csvdata, delimiter=";")

        t411_a = task_411_a(reader, "Final consumption expenditure")
        t411_b = task_411_b(reader)
        t411_2 = task_411_2(reader, "Egypt", "Australia", "Cuba", force_country_limit=True)

        for row in reader:
            parsed_data = parse_data(data_row=row)

main(args.filename)