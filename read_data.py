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
    

def main(filename: str):
    
    with open(filename, newline='') as csvdata:
        reader = DictReader(csvdata, delimiter=";")

        t411_a = task_411_a(reader, "Final consumption expenditure")
        t411_b = task_411_b(reader)

        for row in reader:
            parsed_data = parse_data(data_row=row)

main(args.filename)