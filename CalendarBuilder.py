#!/usr/bin/python

import argparse
from HTMLParser import HTMLParser

class CalendarBuilder(HTMLParser):
    '''Parses an HTML file (containing a dalonline calendar),
    and writes an iCal file containing the events'''

    def __init__(self):
        HTMLParser.__init__(self)
        self.dayofweek = 0
        self.state = 'FINDEVENT'
        self.eventclassname = 'dddefault'

    def find_event(self, tag, attrs):
        for key, value in attrs:
            if key == 'class':
                if value == self.eventclassname:
                    return 'EVENTFOUND'
        return 'FINDEVENT'

    def check_event(self, tag, attrs):
        if tag == 'a':
            return 'GETNAME'
        else:
            raise Exception("Unexpected tag");

    def ignore_tag(self, tag, attrs):
        return self.state

    def invalid_event(self, data):
        return 'FINDEVENT'

    def get_event_name(self, data):
        print "Event: %s" % data
        return 'GETID'

    def get_event_id(self, data):
        print "ID: %s" % data
        return 'GETTIME'
        
    def get_event_time(self, data):
        print "Time: %s" % data
        return 'GETLOCATION'

    def get_event_location(self, data):
        print "Location: %s" % data
        return 'FINDEVENT'

    def ignore_data(self, data):
        return self.state

    def handle_starttag(self, tag, attrs):
        self.state = { 'FINDEVENT':   self.find_event,
                       'EVENTFOUND':  self.check_event,
                       'GETNAME':     self.ignore_tag,
                       'GETID':       self.ignore_tag,
                       'GETTIME':     self.ignore_tag,
                       'GETLOCATION': self.ignore_tag,
                       None:          self.ignore_tag,
                     }[self.state](tag, attrs)

    def handle_data(self, data):
        self.state = { 'FINDEVENT':   self.ignore_data,
                       'EVENTFOUND':  self.invalid_event,
                       'GETNAME':     self.get_event_name,
                       'GETID':       self.get_event_id,
                       'GETTIME':     self.get_event_time,
                       'GETLOCATION': self.get_event_location,
                       None:          self.ignore_data,
                     }[self.state](data)

argparser = argparse.ArgumentParser(
    description = 'Convert a dalonline html calendar to iCal format'
)
argparser.add_argument('infile', type=argparse.FileType('r'))
argparser.add_argument('outfile', type=argparse.FileType('w'))
args = argparser.parse_args()


webpage = CalendarBuilder() 
webpage.feed(args.infile.read())

