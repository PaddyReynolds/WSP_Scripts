#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     06/04/2022
# Copyright:   (c) UKPXR011 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
from fnmatch import fnmatch

root = r'\\uk.wspgroup.com\Central Data\Projects\62240xxx\62240948 - HS2 2B M2_M3\14_Land_Referencing_Technical\06_HMLR\EW-192\Registers'
pattern = "*.pdf"
OnlyFiles = []


for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, pattern):
            OnlyFiles.append(os.path.join(path, name))


with open(r"\\uk.wspgroup.com\Central Data\Projects\62240xxx\62240948 - HS2 2B M2_M3\14_Land_Referencing_Technical\06_HMLR\EW-192\Registers\Registers.txt", 'w') as f:
    for item in OnlyFiles:
        f.write("%s\n" % item)

print "Done"