#!/usr/bin/python2
import argparse
from CalendarBuilder import CalendarBuilder

def run():
    argparser = argparse.ArgumentParser(
        description = 'Convert a dalonline html calendar to iCal format'
    )
    argparser.add_argument('infile', type=argparse.FileType('r'))
    argparser.add_argument('outfile', type=argparse.FileType('w'))
    argparser.add_argument('-r', '--recur')
    args = argparser.parse_args()

    builder = CalendarBuilder() 
    if args.recur is not None:
        builder.setEndDate(args.recur)
    builder.parse(args.infile)
    builder.export(args.outfile)

if __name__ == '__main__':
    run()
