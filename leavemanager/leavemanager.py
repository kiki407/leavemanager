# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
from marshmallow import Schema, fields

"""Main module."""

class Configuration(object):
    def __init__(self, days_of_leave, first_name, last_name):
        self.days_of_leave = days_of_leave
        self.first_name = first_name
        self.last_name = last_name
    
    def __repr__(self):
        return f"<{self.days_of_leave} days for {self.first_name} {self.last_name}>"


class ConfigurationSchema(Schema):
    days_of_leave = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    
    @post_load
    def create_configuration(self, data):
        return Configuration(**)


class ConfigurationFile(object):

    def __init__(self):
        self.filepath = str(Path.home().joinpath(".leavemanager"))

    def __get_configuration(self):
        if not os.path.exists(self.filepath):
            return None
        with open(self.filepath, "r") as confighandler:
            configvalues = json.load(confighandler)

        return configvalues

    def __set_configuration(self, config):
        with open(self.filepath, "w") as confighandler:
            json.dump(config, confighandler)

    configuration = property(__get_configuration, __set_configuration)
