#!/usr/bin/env python

import sys
import csv

def read_csv(csv_file):
    """
    """
    with open(csv_file,'rb') as INFILE:
        csv_reader = csv.reader(INFILE)
        for row in csv_reader:
            print "Bio: " + row[8]

if __name__ == "__main__":
    read_csv(sys.argv[1])        
