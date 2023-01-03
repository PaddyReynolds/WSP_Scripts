#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     20/04/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PyPDF2 import PdfFileMerger
import os
import csv

testCSV = r'C:\Users\UKPXR011\Desktop\Scripts\PDF Merge\A101_034.csv'
pdfDir = r'C:\Users\UKPXR011\Desktop\Scripts\PDF Merge'


# open the file in universal line ending mode
with open(testCSV, 'rU') as infile:
  # read the file as a dictionary for each row ({header : value})
  reader = csv.DictReader(infile)
  data = {}
  for row in reader:
    for header, value in row.items():
      try:
        data[header].append(value)
      except KeyError:
        data[header] = [value]

# extract the variables you want
names = data['Notice_Number']
partyID = data['Party_ID']

print len(names)
print len(partyID)




