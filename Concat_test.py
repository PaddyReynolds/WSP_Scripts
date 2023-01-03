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
fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\PCE Work\PCESample20200623\Scratch_Script.gdb\Plots_Lops'

def concatenate(infeature,uniqueField,concField,writeField):
# Process: Concatenate HMLR Ref
    Delimiter = ','
    valueDict = {}
    lastid = -1
    lastvalue = ""
    Cur4 = arcpy.da.SearchCursor(fc1,[concField,uniqueField])
    for row in Cur4:
        id = row[1]
        value = row[0]
        valueDict[id] = value
        if id == lastid:
            value = str(lastvalue) + Delimiter + str(value)
            valueDict[id] = value
        lastid = id
        lastvalue = value
    del Cur4, row

    print valueDict

    with arcpy.da.UpdateCursor(infeature,[uniqueField,writeField]) as updateRows:
        for updateRow in updateRows:
            keyValue = updateRow[0]
            if keyValue in valueDict:
                updateRow[1] = valueDict[keyValue][0]
                updateRows.updateRow(updateRow)
    del updateRows, updateRow

'''
       for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = valueDict[keyValue][0]
            updateRows.updateRow(updateRow)
'''
concatenate(fc1,'UID','UniqueID','Plot_Id_Concat')
