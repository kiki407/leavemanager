# -*- coding: utf-8 -*-

"""Console script for leavemanager."""
import sys
import click
import leavemanager
from leavemanager.configuration import getconf, setconf, get_keys
from leavemanager.utils import slightlybeautify, clickDate
from leavemanager.leavemanager import Leave, AllLeave
from datetime import datetime
from dateutil.parser import parse


@click.group(chain=False)
@click.version_option(version=leavemanager.__version__)
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
@click.argument("date", type=clickDate.DATE)
@click.option("--until", "-t", type=clickDate.DATE)
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
@click.argument("date", type=clickDate.DATE)
def rem(date):
    """
    Removes an entry from leaves
    """
    leave = Leave(date)
    click.echo(leave.remove())


@main.group(chain=False)
def approve():
    """
    Approves leave 
    """
    return 0


@approve.command()
@click.argument("date", type=clickDate.DATE)
def one(date):
    leave = Leave(date)
    click.echo(leave.approve())


@approve.command()
def old():
    """
    Auto approves leaves previous to today 
    """
    leave = AllLeave()
    click.echo(leave.approve_old())


@main.command()
@click.option("--year", "-y", default="current", help="year of leave")
def report(year):
    """
    shows a report of days taken and days left for the year
    """
    leave = AllLeave()
    click.echo(leave.report(year))


@main.command()
@click.option("--year", "-y", default="current", help="year of leave")
def left(year):
    """
    Tell how many days are left
    """
    leave = AllLeave()
    res = leave.left(year=year)
    click.echo(f"{res}")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
