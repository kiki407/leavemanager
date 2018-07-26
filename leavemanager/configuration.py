# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path


class ConfigurationFile(object):

    def __init__(self):
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


def setconf(configdata):
    cfile = ConfigurationFile()
    cfile.configuration = configdata


def getconf():
    cfile = ConfigurationFile()
    return cfile.configuration
