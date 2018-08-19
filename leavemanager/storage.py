from pathlib import Path
from tinydb import TinyDB, Query


class FileStorage(object):
    def __init__(self):
        filepath = Path.home().joinpath(".leavemanager")
        conf = filepath.joinpath("data.json")
        datafile = str(conf)
        self.db = TinyDB(datafile)
        self.leave = Query()

    def get(self, date):
        return self.db.get(leave.rawdate == date)

    def put(self, date, data):
        s = self.db.get(self.leave.rawdate == date)

        if s:
            return False
        else:
            self.db.insert(data)
            return True

    def delete(self, date):
        s = self.db.get(self.leave.rawdate == date)
        if s:
            self.db.remove(doc_ids=[s.doc_id])
            return True
        else:
            return False

    def update(self, date, update):
        self.db.update(update, self.leave.rawdate == date)

    def countdays(self, year):
        return self.db.count(self.leave.year == year)

    def all(self):
        return self.db.all()

    def all_pending(self, year):
        return self.db.search(self.leave.year == year and self.leave.approved == False)

    def search(self, year):
        return self.db.search(self.leave.year == year)
