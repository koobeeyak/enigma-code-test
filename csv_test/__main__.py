#!/usr/bin/env python

import sys
import csv

from dateutil import parser
from datetime import datetime

# rather than hard coding specific column numbers, these can be changed if csv file has different header names
BIO_COLUMN_NAME = "bio"
STATE_COLUMN_NAME = "state"
START_DATE_COLUMN_NAME = "start_date"
START_DATE_DESC_COLUMN_NAME = "start_date_description"
# file names
INFILE_NAME = 'test.csv'
OUTFILE_NAME = 'solution.csv'
STATE_ABBREVIATIONS_FILE_NAME = 'state_abbreviations.csv'

def clean_bio(bio):
    """
    Replaces all whitespace in string with single space.
    """
    words = bio.split()
    cleaned_bio = " ".join(words)
    return cleaned_bio

def generate_state_abbrev_dict():
    """
    From local file state_abbreviations.csv return dict of key: state abbreviations, value: full state name.
    """
    try:
        with open(STATE_ABBREVIATIONS_FILE_NAME, 'rb') as infile:
            csv_reader = csv.reader(infile)
            state_abbrev_dict = {}
            header = True
            for row in csv_reader:
                if header:
                    # skip first iteration to avoid header
                    header = False
                else:
                    # first column has abbreviations, second has full names
                    abbrev = row[0]
                    full_name = row[1]
                    state_abbrev_dict[abbrev] = full_name
            return state_abbrev_dict
    except IOError as error:
        # can't read state abbreviations file, exit the program
        print error
        sys.exit(1)

def get_index(element, l):
    """
    Return index of element in list or None.
    """
    try:
        index = l.index(element)
        return index
    except ValueError:
        return None

def normalize_date(date):
    """
    Normalize date to ISO 8601 (i.e., YYYY-MM-DD) if year, month, and day present.
    Do this taking advantage of dateutil.parser.parse() 'default' optional argument.
    If any year, month, or day is missing, it will default to provided datetime.datetime object.
    So check each part of date twice with different defaults. If anything changes, there is missing info and we won't return it.
    Owe some credit for idea to: http://stackoverflow.com/q/8434854/6142442
    """
    try:
        day_a = parser.parse(date, default = datetime(2015, 1, 1))
    except ValueError:
        # date cannot be parsed at all, it's an arbitrary string
        return None
    day_b = parser.parse(date, default = datetime(2015, 1, 2))
    # compare two different month defaults
    month_a = parser.parse(date, default = datetime(2015, 1, 1))
    month_b = parser.parse(date, default = datetime(2015, 2, 1))
    # compare two different year defaults
    year_a = parser.parse(date, default = datetime(2015, 1, 1))
    year_b = parser.parse(date, default = datetime(2016, 1, 1))
    if day_a == day_b and month_a == month_b and year_a == year_b:
        # there are no differences, e.g. date provided is complete
        # we can return any of the above formatted dates since they are all equal
        return day_a.strftime("%Y-%m-%d")
    else:
        # one of the above reverts to default, indicating a missing datetime field
        return None

def main():
    """
    Read csv file.
    Clean bio, replace state abbreviation with full state name, try to normalize date, and write everything to new file solutions.csv.
    """
    try:
        with open(INFILE_NAME, 'rb') as infile, open(OUTFILE_NAME, 'wb') as outfile:
            csv_reader = csv.reader(infile)
            csv_writer = csv.writer(outfile)
            header = True
            state_abbrev_dict = generate_state_abbrev_dict()
            for row in csv_reader:
                if header:
                    # let's look for the index of all the columns we are interested in by searching the header
                    bio_index = get_index(BIO_COLUMN_NAME, row)
                    state_index = get_index(STATE_COLUMN_NAME, row)
                    start_date_index = get_index(START_DATE_COLUMN_NAME, row)
                    if bio_index == None or state_index == None or start_date_index == None:
                        print "Error: One of headers: 'bio', 'state', or 'start_date' missing from csv file."
                        break
                    # add new column name to header
                    row.append(START_DATE_DESC_COLUMN_NAME)
                    # write header to csv file
                    csv_writer.writerow(row)
                    header = False
                else:
                    # replace "bio" column with cleaned "bio" string
                    row[bio_index] = clean_bio(row[bio_index])
                    # replace "state" column with state abbreviation if it exists
                    state = row[state_index]
                    if state not in state_abbrev_dict.keys():
                        print "Unknown state abbreviation: %s" % state
                    else:
                        row[state_index] = state_abbrev_dict[state]
                    # replace "start_date" column with normalized date if possible
                    start_date = row[start_date_index]
                    row[start_date_index] = normalize_date(start_date)
                    if row[start_date_index] == None:
                        # if we couldn't normalize, add the string to new column "start_date_description"
                        row.append(start_date)
                    else:
                        row.append(None)
                    # write finished row to csv file
                    csv_writer.writerow(row)
    except IOError as error:
        # can't read or write csv, we need to exit
        print error
        sys.exit(1)

if __name__ == "__main__":
    main()
