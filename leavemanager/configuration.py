# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
import click
import pycountry
from leavemanager.utils import clickDate
from workalendar.registry import registry
from datetime import date, datetime


class Countries(object):
    def __init__(self):
        self.supported_countries = {}
        countries = {a.alpha_2: a.name for a in pycountry.countries}
        countries.update({a.code: a.name for a in pycountry.subdivisions})
        for code in registry.region_registry.keys():
            self.supported_countries[code] = countries.get(code, None)

    def get_countries(self):
        return self.supported_countries.values()

    def get_country_code(self, country):
        reverse = {value: key for key, value in self.supported_countries.items()}
        return reverse.get(country, None)


class ConfigurationFile(object):
    def __init__(self):
        self.fmt = "#date#%Y%m%d"
        countries = Countries().get_countries()
        self.keys = (
            ("days_of_leave", click.INT),
            ("first_name", click.STRING),
            ("last_name", click.STRING),
            ("work_on_weekends", click.BOOL),
            ("work_on_public_holidays", click.BOOL),
            ("country_region_for_holidays", click.Choice(countries)),
            ("storage_type", click.Choice(["File"])),
            ("start_of_leave_year", clickDate.DATE),
        )
        self.filepath = Path.home().joinpath(".leavemanager")
        self.conf = self.filepath.joinpath("config.json")

    def __get_configuration(self):
        if not os.path.exists(str(self.conf)):
            return {}
        with open(str(self.conf), "r") as confighandler:
            configvalues = json.load(confighandler)
            for k, v in configvalues.items():
                if isinstance(v,str) and "#date#" in v:
                    configvalues[k] = datetime.strptime(v, self.fmt).date()
        return configvalues

    def __set_configuration(self, config):
        if not self.filepath.exists():
            self.filepath.mkdir(parents=True, exist_ok=True)
        with open(str(self.conf), "w") as confighandler:
            for k, v in config.items():
                if isinstance(v, date):
                    config[k] = v.strftime(self.fmt)
            json.dump(config, confighandler)

    configuration = property(__get_configuration, __set_configuration)


def get_keys():
    cfile = ConfigurationFile()
    return cfile.keys


def setconf(configdata):
    cfile = ConfigurationFile()
    cfile.configuration = configdata


def getconf():
    cfile = ConfigurationFile()
    return cfile.configuration


def get_country_code(country):
    countries = Countries()
    return countries.get_country_code(country)


def get_business_year(year):
    cfile = ConfigurationFile()
