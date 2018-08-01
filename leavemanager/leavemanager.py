# -*- coding: utf-8 -*-

"""Main module."""

from pathlib import Path
from tinydb import TinyDB, Query
from datetime import date
from leavemanager.configuration import getconf


class Leave(object):

    def __init__(self, date, approved=False):
        self.approved = approved
        self.rawdate = date.strftime("%d/%m/%Y")
        self.year = date.year
        filepath = Path.home().joinpath(".leavemanager")
        conf = filepath.joinpath("data.json")
        datafile = str(conf)

        self.db = TinyDB(datafile)

    def __repr__(self):
        approved = "Approved" if self.approved else "Pending"
        date = self.rawdate
        return f"<{date} - {approved}>"

    def store(self):
        approved = "Approved" if self.approved else "Pending"
        data = dict(rawdate=self.rawdate, year=self.year, approved=self.approved)
        leave = Query()
        s = self.db.search(leave.rawdate == data["rawdate"])
        if len(s) > 0:
            storedapproved = s[0]["approved"]
            if storedapproved != self.approved:
                db.update(
                    {"approved": data["approved"]}, leave.rawdate == data["rawdate"]
                )
                return f"updated approval for {self.rawdate} to {approved}."

            else:
                return f"record exists already."
        else:
            self.db.insert(data)
            return f"created leave {self.rawdate} status {approved}."


class AllLeave(object):

    def __init__(self):
        filepath = Path.home().joinpath(".leavemanager")
        conf = filepath.joinpath("data.json")
        datafile = str(conf)
        self.db = TinyDB(datafile)

    def left(self, year):
        if year == "current":
            year = date.today().year
        leave = Query()
        taken = self.db.count(leave.year == year)
        total = int(getconf().get("days_of_leave", 0))
        print(f"year = {year} - {type(year)}")
        print(f"taken = {taken} - {type(taken)}")
        print(f"total = {total} - {type(total)}")
        return f"{total - taken} days left."
