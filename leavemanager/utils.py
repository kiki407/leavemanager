# -*- coding: utf-8 -*-

import click
from datetime import date, datetime
from dateutil.parser import parse

def slightlybeautify(var):
    return " ".join(var.split("_"))


def formatreport(data, year, daysleft):
    reporttitle = f"Leave report for {year}"
    resstr = ["", reporttitle, "-" * len(reporttitle)]
    for key, value in data.items():
        resstr.append("")
        resstr.append(f"{key.capitalize()}")
        resstr.append("-" * len(key))
        if len(value) == 0:
            resstr.append("No leave")
        for days in value:
            resstr.append(f"{days}")
        resstr.append("-" * len(key))
        resstr.append(f"Tot. {len(value)}")
        resstr.append("")
    resstr.append("Left")
    resstr.append("-" * len("Left"))
    resstr.append(daysleft)
    resstr.append("")
    return "\n".join(resstr)


class DateParamType(click.ParamType):
    name = "date"

    def convert(self, value, param, ctx):
        default = datetime.today()
        try:
            return parse(value, fuzzy=True, default=default, dayfirst=True).date()
        except ValueError:
            self.fail("%s is not a valid date" % value, param, ctx)


class clickDate(object):
    DATE = DateParamType()
