from sys import stderr
from BeautifulSoup import BeautifulSoup
from icalendar import Calendar, Event, vRecur
from datetime import datetime, timedelta
import re

class CalendarBuilder:
    def __init__(self):
        self.calendar = Calendar()
        self.calendar.add("version", "2.0")
        self.calendar.add("prodid", "-//levyd//NONSGML CalendarBuilder//EN")

        self.enddate = None

    def addEvent(self, node, date):
        strings = node.findAll(text=True)
        event = Event()

        event.add("summary", strings[0])

        match = re.search("(\d\d?:\d\d [ap]m)-(\d\d?:\d\d [ap]m)", strings[2])
        if match is None:
            print >> stderr, "Warning: Could not parse time string, %s" % strings[2]
            return False
        else:
            event.add("dtstart", datetime.strptime(date + match.group(1), "%Y-%m-%d %I:%M %p"))
            event.add("dtend", datetime.strptime(date + match.group(2), "%Y-%m-%d %I:%M %p"))
        if self.enddate is not None:
            recur = vRecur(freq="WEEKLY", until=self.enddate)
            event.add("rrule", recur, encode=0)

        event.add("location", strings[3])

        self.calendar.add_component(event)

    def setEndDate(self, enddate):
        self.enddate = datetime.strptime(enddate, "%b %d %Y")

    def parse(self, infile):
        """Parses the dalonline HTML into a schedule for one week"""
        doc = BeautifulSoup(infile.read())

        # Get the base date (Monday) of the webpage's calendar
        weekoftag = doc.find(text=re.compile("Week of .*"))
        weekofre = re.search("Week of (.*)", weekoftag)
        if weekofre is None:
            raise Exception("Fatal: Couldn't determine calendar base date")
        else:
            weekof = datetime.strptime(str(weekofre.group(1)), "%b %d, %Y").strftime("%Y %W")

        dow = 1
        dowcounter = [0, 0, 0, 0, 0, 0, 0]

        # Identify all events in the webpage's calendar
        table = doc.find("table", attrs={"class" : "datadisplaytable"})
        for row in table.findAll("tr"):
            for entry in row.findAll("td"):
                if entry["class"] == "ddlabel":
                    date = datetime.strptime(weekof + " " + str(dow), "%Y %W %w").strftime("%Y-%m-%d ")
                    self.addEvent(entry, date)
                    dowcounter[dow] += int(entry["rowspan"]) - 1
                dow = (dow + 1) % 7
                while dowcounter[dow] > 0:
                    dowcounter[dow] -= 1
                    dow = (dow + 1) % 7
            if dow != 1:
                print >> stderr, "Warning, day-of-week might be misaligned"

    def export(self, outfile):
        outfile.write(self.calendar.as_string())
