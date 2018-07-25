# -*- coding: utf-8 -*-

"""Console script for leavemanager."""
import sys
import click
from leavemanager import configuration


@click.group(chain=True)
def main(args=None):
    """Console script for leavemanager."""
    click.echo(
        "Replace this message by putting your code into " "leavemanager.cli.main"
    )
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


@main.command()
def configure():
    actualconfig = leavemanager.configure()
    if actualconfig:
        click.echo("Modify configuration")
        for k in actualconfig.get_keys():
            val = click.promt(
                f"{actualconfig.get_displayname()}: ".capitalize(),
                default=actualconfig.get_value(),
            )
            actualconfig.set_value(k)
    click.echo("Configuration")


@main.command()
def sim():
    click.echo("simulation mode")


@main.command()
@click.argument("date")
@click.option("--until", "-t")
def add(date, until):
    click.echo("add leave")


@main.command()
def rem():
    click.echo("remove leave")


@main.command()
@click.option("--year", "-y", default="current", help="year of leave")
def left(year):
    click.echo(f"{year}")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
