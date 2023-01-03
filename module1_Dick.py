#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     10/05/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#PYTHON SCRIPT
import arcgisscripting
gp = arcgisscripting.create(93)

d = gp.GetInstallInfo('desktop')
keys = d.keys()
keys.sort()

for k in keys:
    print "%s : %s" % (k, d[k])

import os
os.system("pause")

