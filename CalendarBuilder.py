#!/usr/bin/python
from HTMLParser import HTMLParser

class CalendarBuilder(HTMLParser):
    '''Parses an HTML file (containing a dalonline calendar),
    and writes an iCal file containing the events'''

    def __init__(self):
        HTMLParser.__init__(self)
        self.dayofweek = 0
        self.state = 'FINDEVENT'
        self.eventclassname = 'ddlabel'

    def find_event(self, tag, attrs):
        if tag == "td":
            for key, value in attrs:
                if key == 'class' and value == self.eventclassname:
                    #print self.get_starttag_text()
                    return 'EVENTFOUND'
        return 'FINDEVENT'

    def check_event(self, tag, attrs):
        if tag == 'a':
            return 'GETNAME'
        else:
            raise Exception.NotImplemented

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
        #print "Tag: Initial state: %s" % self.state
        self.state = { 'FINDEVENT':   self.find_event,
                       'EVENTFOUND':  self.check_event,
                       'GETNAME':     self.ignore_tag,
                       'GETID':       self.ignore_tag,
                       'GETTIME':     self.ignore_tag,
                       'GETLOCATION': self.ignore_tag,
                       None:          self.ignore_tag,
                     }[self.state](tag, attrs)
        #print "Tag: State changed to: %s" % self.state

    def handle_data(self, data):
        #print "Data: Initial state: %s" % self.state
        self.state = { 'FINDEVENT':   self.ignore_data,
                       'EVENTFOUND':  self.ignore_data,
                       'GETNAME':     self.get_event_name,
                       'GETID':       self.get_event_id,
                       'GETTIME':     self.get_event_time,
                       'GETLOCATION': self.get_event_location,
                       None:          self.ignore_data,
                     }[self.state](data)
        #print "Data: State changed to: %s" % self.state

