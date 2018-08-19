# -*- coding: utf-8 -*-

"""Main module."""

from pathlib import Path
from tinydb import TinyDB, Query
from datetime import date, datetime
from leavemanager.configuration import getconf, get_country_code
from leavemanager.utils import formatreport
from leavemanager.storage import FileStorage
from workalendar.registry import registry


class Leave(object):
    def __init__(self, date, approved=False):
        self.date = date
        self.approved = approved
        self.rawdate = date.strftime("%d/%m/%Y")
        self.year = date.year
        self.business_year = self.business_year(date)
        self.storage = FileStorage()

    def __repr__(self):
        approved = "Approved" if self.approved else "Pending"
        date = self.rawdate
        return f"<{date} - {approved}>"

    def is_working_day(self):
        conf = getconf()
        country = conf["country_for_holidays"]
        country_code = get_country_code(country)
        if country_code:
            cal = registry.get_calendar_class(country_code)()
            return cal.is_working_day(self.date)
        else:
            return

    def is_holliday(self):
        conf = getconf()
        country = conf["country_for_holidays"]
        country_code = get_country_code(country)
        if country_code:
            cal = registry.get_calendar_class(country_code)()
            return cal.is_holliday(self.date)
        else:
            return

    def remove(self):
        if self.storage.delete(self.rawdate):
            return f"Removed {self.rawdate} from list"
        else:
            return f"No leave found for date {self.rawdate}"

    def approve(self):
        if self.storage.update(self.rawdate, {"approved": True}):
            return f"{self.rawdate} marked approved"
        else:
            return f"nothing to approve for the date {self.rawdate}"

    def store(self):
        conf = getconf()
        approved = "Approved" if self.approved else "Pending"
        data = dict(rawdate=self.rawdate, year=self.year, approved=self.approved)
        if not conf.get("work_on_public_holidays", False):
            if not conf.get("work_on_weekends", False):
                if not self.is_working_day():
                    return f"({self.rawdate}) is on a weekend"
            else:
                if self.is_holliday():
                    return f"({self.rawdate}) seems to be on a public holiday"
        if self.storage.put(self.rawdate, data):
            return f"{self.rawdate} added"


class LeaveRange(object):
    def __init__(self, date, until, approved=False):
        self.date = date
        self.until = until
        self.approved = approved
        self.rawdate = date.strftime("%d/%m/%Y")
        self.rawuntil = until.strftime("%d/%m/%Y")
        self.year = date.year
        self.storage = FileStorage()

    def __repr__(self):
        approved = "Approved" if self.approved else "Pending"
        date = self.rawdate
        until = self.rawuntil
        return f"<{date} -> {until}- {approved}>"


class AllLeave(object):
    def __init__(self):
        self.storage = FileStorage()

    def left(self, year):
        if year == "current":
            year = date.today().year
        leave = Query()
        taken = self.storage.countdays(year)
        total = int(getconf().get("days_of_leave", 0))
        return f"{total - taken} days left."

    def approve_old(self):
        leave = Query()
        today = date.today()
        for rowleave in self.storage.all():
            print(rowleave)
            leavedate = datetime.strptime(rowleave["rawdate"], "%d/%m/%Y").date()
            if leavedate < today:
                self.storage.update({"approved": True}, rowleave["rawdate"])

    def report(self, year, format=None):
        if year == "current":
            year = date.today().year
        else:
            year = int(year)
        today = date.today()
        leave = Query()
        res = {}
        for rowleave in self.storage.search(year):
            leavedate = datetime.strptime(rowleave["rawdate"], "%d/%m/%Y").date()
            if leavedate < today:
                if "taken" in res.keys():
                    res["taken"].append(rowleave["rawdate"])
                else:
                    res["taken"] = [rowleave["rawdate"]]
            else:
                if rowleave["approved"]:
                    if "approved" in res.keys():
                        res["approved"].append(rowleave["rawdate"])
                    else:
                        res["approved"] = [rowleave["rawdate"]]
                else:
                    if "pending" in res.keys():
                        res["pending"].append(rowleave["rawdate"])
                    else:
                        res["pending"] = [rowleave["rawdate"]]
        return formatreport(res, year, self.left(year))
