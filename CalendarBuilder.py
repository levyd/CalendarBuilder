from BeautifulSoup import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime
import re

class CalendarBuilder:
    def __init__(self):
        self.calendar = Calendar()

    def parse(self, infile):
        """Parses the dalonline HTML into a schedule for one week"""
        doc = BeautifulSoup(infile.read())

        # Get the base date (Monday) of the webpage's calendar
        weekoftag = doc.find(text=re.compile("Week of .*"))
        weekofre = re.search("Week of (.*)", weekoftag)
        if weekofre is None:
            raise Exception("Oh shit")
        else:
            weekof = str(weekofre.group(1))
            print "Base day: %s" % weekof

        # Identify all events in the webpage's calendar
        for entry in doc.findAll("td", attrs={"class" : "ddlabel"}):
            strings = entry.findAll(text=True)
            event = Event()

            print "Summary: %s" % strings[0]
            event.add("summary", strings[0])

            print "Time: %s" % strings[2]
            match = re.search("(\d\d?:\d\d [a|p]m)-(\d\d?:\d\d [a|p]m)", strings[2])
            if match is None:
                continue
            else:
                event.add("dtstart", datetime.strptime(weekof + match.group(1), "%b %d, %Y%I:%M %p")) # Plus dow
                event.add("dtend", datetime.strptime(weekof + match.group(2), "%b %d, %Y%I:%M %p"))

            print "Location: %s" % strings[3]
            self.calendar.add_component(event)

    def repeat(self, begindate, enddate):
        pass

    def export(self, outfile):
        outfile.write(self.calendar.as_string())
