# -*- coding: utf-8 -*-


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
