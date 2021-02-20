from csv import DictReader
from functools import namedtuple
from argparse import ArgumentParser
import matplotlib.pyplot as plt

parser = ArgumentParser()
parser.add_argument("--filename", "-if", type=str, help="Input file")
args = parser.parse_args()

info_data = namedtuple("info", "cid country iname years data")

class GDP:

    def __init__(self, data):
        self.data = data

    def _remove_headings(self) -> dict:

        data.pop("ï»¿CountryID")
        data.pop("Country")
        data.pop("IndicatorName")

        return data

    def _parse_gdp(self, data: str) -> int:
	    return int(data.replace(".", ""))

    def parse_data(self) -> namedtuple:

        cid, country, iname = self.data["ï»¿CountryID"], self.data["Country"], self.data["IndicatorName"]
        years = {k: self._parse_gdp(v) for k, v in self._remove_headings(data_row).items() if v != ""}
        data = list(filter(None, [years[year] for year in years.keys()]))

        return info_data(cid, country, iname, years, data)

    def _count(self, row):

        c = 0
        for year, num in row.items():
            if not num:
                c += 1

        return c

    def task_411_a(self, iname: str) -> list:
        ret = []

        for row in self.data:

            if row["IndicatorName"] == iname:
                c = self._count(row)
                result = 50 - c

                ret.append(
                    (row["Country"], result)
                )

        return ret

    def task_411_b(self) -> tuple:

        cc = 0

        for row in self.data:

            if row["IndicatorName"] == "Final consumption expenditure":

                c   = self._count(row)
                res = 50 - c

                if res == 50:
                    cc += 1

        percentage = round(((220 - cc) * 100) / 220, 2)

        return cc, percentage

    def task_411_2(self, *countries, force_country_limit=False) -> list:

        def ignore_headings(data: dict) -> dict:
            return {k: v for k, v in data.items() if k != "ï»¿CountryID" and k != "Country" and k != "IndicatorName"}

        if force_country_limit and len(countries) != 3:
            raise ValueError("You must provide 3 countries")

        all_exports = []
        all_imports = []

        for row in self.data:
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
            ret = []

            for x, y in zip(exports[1].values(), imports[1].values()):
                x = self._parse_gdp(x)
                y = self._parse_gdp(y)
                ret.append(x - y)

            net_exports.append(
                (country, {str(i): v for i, v in enumerate(ret, 1970)})
            )

        return net_exports

        # ret      = [(sd(x) - sd(y)) for e, i in zip(all_exports, all_imports) for x, y in zip(e[1].values(), i[1].values()) if (sd := lambda x: int(x.replace(".", "")))]
        # splitted = [ret[i: i + 50] for i in range(0, len(ret), 50)]
        # print(splitted)

def main(filename: str):
    with open(filename, newline='') as csvdata:
        reader = DictReader(csvdata, delimiter=';')

        gdp = GDP(reader)
        print(gdp.task_411_2("Egypt", "Australia", "Cuba", "Germany"))

main(args.filename)