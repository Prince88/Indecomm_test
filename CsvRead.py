#!/usr/bin/python2.7

# Unittest run if file is run without any cmd line input
# Result  displayed in case of a valid file is supplied as in input
# Required files 'test_share_data.csv' and 'badcsvfile.csv' and 'Missing_value.csv' must be located in the same directory


# In case of any missing value for any column, Exception BadInputFile is raised
# In case of bad field names (Missing Year/Month), Exception BadInputFile is raised
# Last relevant Month/Year is considered in case of multiple highest share price

import csv
import sys

class BadInputFile(Exception):
    """Exception class for bad file type"""
    
    def __init__(self,filename):
        self.filename = filename

    def __str__(self):
        return "Bad input file: '{}'".format(self.filename)



def ParseData(filename):
    '''
        Funtion responsible for:
         1) Exception handle while opening the file
         2) Printing the required output
    '''
    actualResult = {}
    try:
        fh = open(filename,'r')
        reader = csv.DictReader(fh) #Try and open the file with csv dictreader

        #Get the field names in the file: Will help verify if fields needed are there or not
        fields = set(reader.fieldnames)
        if not fields or 'Year' not in fields or 'Month' not in fields:
            raise BadInputFile(filename)
        companies = fields - {'Year', 'Month'}
        companies = list(companies)

        # Check if any field for any Company name has a missing value
        # We can remove this piece of code and can form the result with
        # remaining values for that company.
        for obj in reader:
            for name in companies:
                if obj[name] == '':
                    raise BadInputFile(filename)
        fh.seek(0)
        fh.next()
        
        for name in companies:
            #sorting the csv file data based on column data with Company Name as Key
            result = sorted(reader, key=lambda d: float(d[name]), reverse=True)
            result = result[0]
            tup = (result[name],result['Year'],result['Month'])
            actualResult.update({str(name): tup})
            fh.seek(0) #rewinding the file to initial position
            fh.next()  #Moving to the 1st row -- with field names
    except (IOError, BadInputFile) as e:
        print "Error: ", str(e) # Invalid input file
        raise


    return actualResult


def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        print "No input file given. Run unit test\n"
        unittest.main()
    else:
        print "Parsing the CSV file"
        result = ParseData(filename)
        print result

# Since the exact environment of the script testing is unknown, testing
# code has been included within the same file so as to provide seamless
# testing

# Tests run incase of no file is provided as input

import unittest

class TestPraseData(unittest.TestCase):

    def setUp(self):
    # Expected output for the declared file
        self.expectedData = {'Company-E': ('870', '1990', 'Jul'),
                        'Company-D': ('941', '1990', 'Jul'),
                        'Company-C': ('917', '1991', 'Feb'),
                        'Company-B': ('914', '1990', 'Apr'),
                        'Company-A': ('969', '1990', 'Aug')}

    def test_Output(self):
        '''Check the output'''
        Data = ParseData("test_shares_data.csv")
        self.assertEqual(self.expectedData, Data)


    def test_IoError(self):
        '''check for IoError'''
        with self.assertRaises(IOError):
            ParseData("Non-ExistingFile")

    def test_IfProperFieldnames(self):
        '''Check for BadInputFile -- File with not poper fields'''
        with self.assertRaises(BadInputFile):
            ParseData("BadCsvFile.csv")

    def test_IfMissingValue(self):
        '''Check for BadInputFile -- File that has missing value in any company column'''
        
        with self.assertRaises(BadInputFile):
            ParseData("Missing_Data.csv")


if __name__ == '__main__':
    main()
    
