#!/usr/bin/python2
import argparse
from CalendarBuilder import CalendarBuilder

def run():
    argparser = argparse.ArgumentParser(
        description = 'Convert a dalonline html calendar to iCal format'
    )
    argparser.add_argument('infile', type=argparse.FileType('r'))
    argparser.add_argument('outfile', type=argparse.FileType('w'))
    args = argparser.parse_args()


    webpage = CalendarBuilder() 
    webpage.feed(args.infile.read())
    args.outfile.write(webpage.calendar.as_string())

if __name__ == '__main__':
    run()
