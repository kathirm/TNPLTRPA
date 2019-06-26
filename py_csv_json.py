import json, sys, os
import csv


def csvtoJsonconvert():
    try:
        print "upload csv file"
        with open('convertion.csv') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            print "get csv rows value ==> %s"%rows
            for row in rows:
                print row['Qualification']        
    except Exception as er:
        print "Exception throws error ==> %s"%er


csvtoJsonconvert()
