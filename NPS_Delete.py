#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     22/01/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

fc1 = r'C:\Users\UKPXR011\Desktop\Safeguarding\NPS\Scratch.gdb\LandOwnershipDissolved_NPS'

fc2 =r'C:\Users\UKPXR011\Desktop\Safeguarding\NPS\National_Polygon_Service\National_Polygon_Service_January2020_FullSupply\National_Polygon_Service_January2020_FullSupply.gdb\GEODATA\NPD_January2020_FullSupply'

valueDict = {r[0] for r in arcpy.da.SearchCursor(fc1,['TITLE_NO'])}

with arcpy.da.UpdateCursor(fc2, ['TITLE_NO']) as updateRows:

    for updateRow in updateRows:

        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            pass
        else:
            updateRows.deleteRow()