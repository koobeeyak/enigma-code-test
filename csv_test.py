#!/usr/bin/env python

import sys
import csv

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
        with open("state_abbreviations.csv", 'rb') as INFILE:
            csv_reader = csv.reader(INFILE)
            state_abbrev_dict = {}
            header = True
            for row in csv_reader:
                if header:
                    # skip first iteration to avoid header
                    header = False
                    continue
                else:
                    # first column has abbreviations, second has full names
                    abbrev = row[0]
                    full = row[1]
                    state_abbrev_dict[abbrev] = full
            return state_abbrev_dict
    except IOError as error:
        print error
    

def read_and_write_csv(csv_file):
    """
    """
    try:
        with open(csv_file, 'rb') as INFILE:
            csv_reader = csv.reader(INFILE)
            header = True
            for row in csv_reader:
                if header:
                    # do not make any changes to header
                    header = False
                    continue
                else:
                    print "Bio: " + row[8]
                    print "New Bio " + clean_bio(row[8])
    except IOError as error:
        print error

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # we need a filename to be passed
        print "Usage:" 
        print "$ python csv_test.py test.csv"
    else:
        read_and_write_csv(sys.argv[1])
