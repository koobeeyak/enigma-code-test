# csv\_test
##Purpose
1. Read arbitrary csv file from argument
2. Try to find "bio", "state", and "start\_date" columns
3. Write new csv file with:
  * "bio" column cleaned of unnecessary whitespace
  * "state" column abbreviations replaced with full state names from 'state\_abbreviations.csv'
  * "start\_date" column containing only full dates in ISO 8601 (YYYY-MM-DD) format
 * additional "start\_date\_description" column containing leftover incomplete dates

##Usage
    $ python . test.csv

