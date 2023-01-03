#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     26/06/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\PCE Work\Scratch.gdb\Schema_27062020'
#The field to base the concatenation on
a = 'LandOwnershipParcels'
#The field holding the values to concatenate
b = 'InterestHoldersName'
#The field to hold the concatenation
c = 'Names_Concat'


def concatenate(infeature,uniqueField,concField,writeField):
# Process: Concatenate HMLR Ref
    Delimiter = ','
    Uni_V_Dictionary = {}
    lastid = -1
    lastvalue = ""
    Cur4 = arcpy.da.SearchCursor(fc1,[concField,uniqueField])
    for row in Cur4:
        id = row[1]
        value = row[0]
        Uni_V_Dictionary[id] = value
        if id == lastid:
            value = str(lastvalue) + Delimiter + str(value)
            Uni_V_Dictionary[id] = value
        lastid = id
        lastvalue = value
    del Cur4, row
    cur2 = arcpy.UpdateCursor(infeature)
    for row in cur2:
        id = str(row.getValue(uniqueField))
        row.setValue(writeField, Uni_V_Dictionary[id])
        cur2.updateRow(row)
    del cur2, row

concatenate(fc1,a,b,c)
