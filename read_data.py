from csv import DictReader, reader
from functools import namedtuple
from argparse import ArgumentParser
import matplotlib.pyplot as plt
from copy import deepcopy
from itertools import tee
from pprint import pprint
from numpy import arange
from matplotlib.axis import XAxis

parser = ArgumentParser()
parser.add_argument("--filename", "-if", type=str, help="Input file")
args = parser.parse_args()

info_data = namedtuple("info", "cid country iname years data")

class GDP:

    def __init__(self, data: list):
        self.data = data
        self.all_countries = [
            row["Country"] for row in data
            if row["IndicatorName"] == "Final consumption expenditure"
        ]

    def _remove_headings(self) -> dict:

        data.pop("ï»¿CountryID")
        data.pop("Country")
        data.pop("IndicatorName")

        return data

    def _parse_gdp(self, data: str) -> int:
        return int(data.replace(".", ""))

    def _ignore_headings(self, data: dict) -> dict:
        return {k: v for k, v in data.items() if k != "ï»¿CountryID" and k != "Country" and k != "IndicatorName"}

    def _count(self, row):

        c = 0
        for year, num in row.items():
            if not num:
                c += 1

        return c

    def _countries_exist(self, countries: list) -> bool:

        for country in countries:
            if country not in self.all_countries:
                return False

        return True

    def _non_existing_countries(self, countries: list) -> list:
        return [country for country in countries if country not in self.all_countries]

    def parse_data(self) -> namedtuple:

        cid, country, iname = self.data["ï»¿CountryID"], self.data["Country"], self.data["IndicatorName"]
        years = {k: self._parse_gdp(v) for k, v in self._remove_headings(data_row).items() if v != ""}
        data = list(filter(None, [years[year] for year in years.keys()]))

        return info_data(cid, country, iname, years, data)

    def task_411_a(self, iname: str, plot: bool=False) -> list:
        ret = []

        for row in self.data:

            if row["IndicatorName"] == iname:
                c = self._count(row)
                result = 50 - c

                ret.append(
                    (row["Country"], result)
                )

        if plot:
            plt.bar([i for i in range(len(ret))], [v[1] for v in ret])
            plt.show()

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

    def task_412(
        self, 
        *countries, 
        force_country_limit=False, 
        plot               =False
    ) -> list:

        if not self._countries_exist(list(countries)):
            nec = self._non_existing_countries(list(countries))
            raise ValueError(f"The countrie(s) \"{', '.join(nec)}\" do not exist.")

        if force_country_limit and len(countries) != 3:
            raise ValueError("You must provide 3 countries")

        all_exports = []
        all_imports = []

        for row in self.data:
            for country in countries:

                if row["Country"] == country and row["IndicatorName"] == "Exports of goods and services":
                    exports = self._ignore_headings(row)
                    all_exports.append((country, exports))
                elif row["Country"] == country and row["IndicatorName"] == "Imports of goods and services":
                    imports = self._ignore_headings(row)
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

        if plot:

            fig, axs = plt.subplots(len(net_exports), 1, figsize=(18, 8), sharex=True)
            #fig.tight_layout()
            
            if len(countries) > 1:
                for i, (c, v) in enumerate(net_exports):
                    #axs[i].bar([i for i in range(len(v))], v.values())
                    axs[i].bar(v.keys(), v.values())
                    axs[i].yaxis.set_label_position('right')
                    axs[i].set_ylabel(c, rotation=0, labelpad=len(c) << 2)
                    axs[i].tick_params(axis='x', labelrotation=90)
            else:
                #axs.bar([i for i in range(len(net_exports[0][1]))], net_exports[0][1].values())
                axs.bar(net_exports[0][1].keys(), net_exports[0][1].values())
                plt.xticks(rotation=90)
                axs.set_title(net_exports[0][0])
            #plt.savefig('file.png', dpi=200)
            plt.show()


        return net_exports

        # ret      = [(sd(x) - sd(y)) for e, i in zip(all_exports, all_imports) for x, y in zip(e[1].values(), i[1].values()) if (sd := lambda x: int(x.replace(".", "")))]
        # splitted = [ret[i: i + 50] for i in range(0, len(ret), 50)]
        # print(splitted)

    def setup(self, x, r: int=1, gdp_parsed: bool=False) -> list: #0x3B9ACA00

        if gdp_parsed:
            return [v / r for v in self._ignore_headings(x[0][1]).values()]

        return [self._parse_gdp(v) / r for v in self._ignore_headings(x[0]).values()]

    def net_exports(self, country, r: int=1):
        return self.setup(self.task_412(country), r=r, gdp_parsed=True)

    def get_hce(self, country, r: int=1) -> list:
        return self.setup(
            [row for row in self.data if row["IndicatorName"].startswith("Household consumption expenditure") and row["Country"] == country],
            r=r
        )

    def get_gdfce(self, country, r: int=1) -> list:
        return self.setup(
            [row for row in self.data if row["IndicatorName"] == "General government final consumption expenditure" and row["Country"] == country],
            r=r
        )

    def get_gcf(self, country, r: int=1) -> list:
        return self.setup(
            [row for row in self.data if row["IndicatorName"] == "Gross capital formation" and row["Country"] == country],
            r=r
        )

    def task_413_b(self, *countries):

        if not self._countries_exist(list(countries)):
            nec = self._non_existing_countries(list(countries))
            raise ValueError(f"The countrie(s) \"{', '.join(nec)}\" do not exist.")

        if len(countries) < 1:
            raise ValueError("List 'countries' must contain at least one country")

        fig, axs = plt.subplots(len(countries), 1, sharex=True)

        if len(countries) == 1:
            axs = [axs]

        for i, country in enumerate(countries):

            label = [i for i in range(1970, 2020)]

            _net_exports_y = self.net_exports(country, r=0x3B9ACA00)
            _hce_y         = self.get_hce(country, r=0x3B9ACA00)
            _gdfce_y       = self.get_gdfce(country, r=0x3B9ACA00)
            _gcf_y         = self.get_gcf(country, r=0x3B9ACA00)

            axs[i].xaxis.set_ticks(arange(1970, 2020, 1))
            axs[i].axhline(0, color='black')
            axs[i].tick_params(axis='x', labelrotation=90)
            axs[i].yaxis.set_label_position("right")
            axs[i].set_ylabel(country, rotation=0, labelpad=len(country) << 2)

            axs[i].plot(label, _net_exports_y, ".-", label='Net exports')
            axs[i].plot(label, _hce_y, ".-", label='HCE')
            axs[i].plot(label, _gdfce_y, ".-", label='GDFCE')
            axs[i].plot(label, _gcf_y, ".-", label='GCF')

            handels, labels = axs[i].get_legend_handles_labels()
            
        fig.legend(handels, labels, loc='upper left')
        plt.show()

    def calculate_gdp(self, *countries) -> list:

        ret = []
        
        for country in countries:
            net_exports = self.net_exports(country, r=1000000000)
            hce         = self.get_hce(country,     r=1000000000)
            gdfce       = self.get_gdfce(country,   r=1000000000)
            gcf         = self.get_gcf(country,     r=1000000000)

            gdp = []

            for _nexports, _hce, _gdfce, _gcf in zip(net_exports, hce, gdfce, gcf):
                _gdp = _nexports + _hce + _gdfce + _gcf
                gdp.append(_gdp)

            ret.append(
                (country, {str(i): v for i, v in enumerate(gdp, 1970)})
            )

        return ret

    def gdp_proportion(self, *countries) -> list:

        gdp       = self.calculate_gdp(*countries)
        comp_data = namedtuple("cdata", "hce gdfce gcf")
        ret       = []

        for country, data in gdp:
            hce   = self.get_hce(country,   r=1000000000)
            gdfce = self.get_gdfce(country, r=1000000000)
            gcf   = self.get_gcf(country,   r=1000000000)

            d = []

            for g, _hce, _gdfce, _gcf in zip(data.values(), hce, gdfce, gcf):
                __hce   = round(_hce / g, 2)
                __gdfce = round(_gdfce / g, 2)
                __gcf   = round(_gcf / g, 2)

                d.append((__hce, __gdfce, __gcf))

            ret.append(
                (country, {str(i): comp_data(_hce, _gdfce, _gcf) for i, (_hce, _gdfce, _gcf) in enumerate(d, 1970)})
            )

        return ret

    def task_414_a(self, *countries) -> list:
        pass

    def task_414_b(self):
        pass


def main(filename: str):
    with open(filename, newline='') as csvdata:
        reader = DictReader(csvdata, delimiter=';')
        data = list(reader)

    gdp = GDP(data)
    #ret = gdp.task_412("Germany", "Egypt", "Australia", plot=True)
    r = gdp.gdp_proportion("Egypt", "Australia")
    print(r)
    #gdp.task_413_b("Egypt", "Germany")

main(args.filename)