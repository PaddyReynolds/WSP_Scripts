#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     15/07/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\M2M3_DRC_Mailing_List\GSSGISK-463\Scratch.gdb\CP2_1_Tunnels'


def add_average_width(featureClass, averageWidthField):
    '''
    (str, [str]) -> str

    Calculate the average width of each feature in the feature class. The width
        is reported in units of the feature class' projected coordinate systems'
        linear unit.

    Returns the name of the field that is populated with the feature widths.
    '''
    import arcpy
    from math import pi

    # Add the width field, if necessary
    fns = [i.name.lower() for i in arcpy.ListFields(featureClass)]
    if averageWidthField.lower() not in fns:
        arcpy.AddField_management(featureClass, averageWidthField, 'DOUBLE')

    fnsCur = ['SHAPE@LENGTH', 'SHAPE@AREA', averageWidthField]
    with arcpy.da.UpdateCursor(featureClass, fnsCur) as cur:
        for row in cur:
            perim, area, width = row
            row[-1] = ((perim/pi) * area) / (perim**2 / (4 * pi))
            cur.updateRow(row)

    return averageWidthField


add_average_width(fc1,'Width')