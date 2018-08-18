# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
import click
import pycountry
from workalendar.registry import registry


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
        countries = Countries().get_countries()
        self.keys = (
            ("days_of_leave", click.INT),
            ("first_name", click.STRING),
            ("last_name", click.STRING),
            ("work_on_weekends", click.BOOL),
            ("work_on_public_holidays", click.BOOL),
            ("country_for_holidays", click.STRING),
            ("storage_type", click.Choice(countries)),
        )
        self.filepath = Path.home().joinpath(".leavemanager")
        self.conf = self.filepath.joinpath("config.json")

    def __get_configuration(self):
        if not os.path.exists(str(self.conf)):
            return {}
        with open(str(self.conf), "r") as confighandler:
            configvalues = json.load(confighandler)

        return configvalues

    def __set_configuration(self, config):
        if not self.filepath.exists():
            self.filepath.mkdir(parents=True, exist_ok=True)
        with open(str(self.conf), "w") as confighandler:
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
