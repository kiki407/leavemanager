# -*- coding: utf-8 -*-

"""Console script for leavemanager."""
import sys
import click
from leavemanager.configuration import getconf, setconf
from leavemanager.utils import slightlybeautify
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


@click.group(chain=True)
def main(args=None):
    """Console script for leavemanager."""
    return 0


@main.command()
def configure():
    keys = (
        ("days_of_leave", click.INT),
        ("first_name", click.STRING),
        ("last_name", click.STRING),
        ("storage_type", click.Choice(["file"])),
    )
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
def add(date, until):
    click.echo(f"{date}")


@main.command()
def rem():
    click.echo("remove leave")


@main.command()
@click.option("--year", "-y", default="current", help="year of leave")
def left(year):
    click.echo(f"{year}")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
