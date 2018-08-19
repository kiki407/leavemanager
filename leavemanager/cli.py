# -*- coding: utf-8 -*-

"""Console script for leavemanager."""
import sys
import click
from leavemanager.configuration import getconf, setconf, get_keys
from leavemanager.utils import slightlybeautify
from leavemanager.leavemanager import Leave, AllLeave
from datetime import datetime
from dateutil.parser import parse


class DateParamType(click.ParamType):
    name = "date"

    def convert(self, value, param, ctx):
        default = datetime.today()
        try:
            return parse(value, fuzzy=True, default=default, dayfirst=True).date()
        except ValueError:
            self.fail("%s is not a valid date" % value, param, ctx)


DATE = DateParamType()


@click.group(chain=False)
def main(args=None):
    """Console script for leavemanager."""
    return 0


@main.command()
def configure():
    """
    Prompts user for configuration settings
    """
    keys = get_keys()
    actualconfig = getconf()
    newconf = {}
    click.echo("Modify configuration")
    for k in keys:
        newconf[k[0]] = click.prompt(
            f"{slightlybeautify(k[0])}".capitalize(),
            default=actualconfig.get(k[0], None),
            type=k[1],
        )
    setconf(newconf)


@main.command()
def sim():
    click.echo("simulation mode")


@main.command()
@click.argument("date", type=DATE)
@click.option("--until", "-t", type=DATE)
@click.option("--approved", "-A", type=click.BOOL)
def add(date, until, approved):
    """
    Adds a new entry in dates of leave
    """
    if until:
        leave = LeaveRange(date, until)
    else:
        leave = Leave(date)
    click.echo(leave.store())


@main.command()
@click.argument("date", type=DATE)
def rem(date):
    leave = Leave(date)
    click.echo(leave.remove())


@main.group()
def approve():
    click.echo("remove leave")


@approve.command()
def old():
    leave = AllLeave()
    leave.approve_old()


@main.command()
@click.option("--year", "-y", default="current", help="year of leave")
def report(year):
    leave = AllLeave()
    click.echo(leave.report(year))


@main.command()
@click.option("--year", "-y", default="current", help="year of leave")
def left(year):
    leave = AllLeave()
    res = leave.left(year=year)
    click.echo(f"{res}")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
