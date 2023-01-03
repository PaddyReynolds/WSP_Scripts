# File name: GSSGISK-2236_Finalise_HS2B_2020_Safeguarding_Script_Manchester.py
# Author: Ollie Brown
# Date created: 20200312
# Date last modified: N/A
# Python Version: 2.7.13

# Import system modules
import arcpy
from datetime import *
from collections import Counter
import operator
import pprint

#Capture start time of script  
start = datetime.now()  
print 'Safeguarding Started: %s\n' % (start)  

# Set global variables
arcpy.env.overwriteOutput = True

# Take a copy of Land Ownerships and move to the working folder so that the input data is not changed in anyway
requiredLOP = r"C:\Users\ukodb001\Desktop\Tasks\2020\GSSGISK-2236_Finalise_HS2B_2020_Safeguarding_Script\ScriptRun\Manchester\HS2B_Safeguarding_2020_Manchester_20200325_092220\Output.gdb\Required_LOP"

# List fields in inputs
requiredLOPfields = [f.name for f in arcpy.ListFields(requiredLOP)]

# Calculate Scenario field
with arcpy.da.UpdateCursor(requiredLOP, requiredLOPfields) as cursor:
    for row in cursor:
        # Scenario 1 - SLOP within Surface SG where Surface SG has changed
        if  row[9] >= 1 and row[9]-row[10] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] < 1:
            row[72] = 1
            row[73] = 'Surface SG'
            row[74] = 'Surface SG has increased'
        if  row[9] >= 1 and row[10]-row[9] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] < 1:
            row[72] = 1
            row[73] = 'Surface SG'
            row[74] = 'Surface SG has decreased'
        # Scenario 2 - SLOP within Surface SG and EHPZ1 where Surface SG has changed
        if  row[9] >= 1 and row[9]-row[10] >= 1 and row[11] < 1 and row[13] >= 1 and row[15] < 1 and row[17] < 1 and row[19] < 1:
            row[72] = 2
            row[73] = 'Surface SG and EHPZ1'
            row[74] = 'Surface SG has increased'
        if  row[9] >= 1 and row[10]-row[9] >= 1 and row[11] < 1 and row[13] >= 1 and row[15] < 1 and row[17] < 1 and row[19] < 1:
            row[72] = 2
            row[73] = 'Surface SG and EHPZ1'
            row[74] = 'Surface SG has decreased'
        # Scenario 3 - SLOP within Surface SG and EHPZ2 where Surface SG has changed
        if  row[9] >= 1 and row[9]-row[10] >= 1 and row[11] < 1 and row[13] < 1 and row[15] >= 1 and row[17] < 1 and row[19] < 1:
            row[72] = 3
            row[73] = 'Surface SG and EHPZ2'
            row[74] = 'Surface SG has increased'
        if  row[9] >= 1 and row[10]-row[9] >= 1 and row[11] < 1 and row[13] < 1 and row[15] >= 1 and row[17] < 1 and row[19] < 1:
            row[72] = 3
            row[73] = 'Surface SG and EHPZ2'
            row[74] = 'Surface SG has decreased'
        # Scenario 4 - SLOP within Surface SG and EHPZ3 where Surface SG has changed
        if  row[9] >= 1 and row[9]-row[10] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] >= 1 and row[19] < 1:
            row[72] = 4
            row[73] = 'Surface SG and EHPZ3'
            row[74] = 'Surface SG has increased'
        if  row[9] >= 1 and row[10]-row[9] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] >= 1 and row[19] < 1:
            row[72] = 4
            row[73] = 'Surface SG and EHPZ3'
            row[74] = 'Surface SG has decreased'
        # Scenario 5 - SLOP within Surface SG and RSZ where Surface SG has changed
        if  row[9] >= 1 and row[9]-row[10] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[71] == 'Yes':
            row[72] = 5
            row[73] = 'Surface SG and RSZ'
            row[74] = 'Surface SG has increased'
        if  row[9] >= 1 and row[10]-row[9] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[71] == 'Yes':
            row[72] = 5
            row[73] = 'Surface SG and RSZ'
            row[74] = 'Surface SG has decreased'
        if  row[9] >= 1 and row[9]-row[10] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[71] <> 'Yes':
            row[72] = 1
            row[73] = 'Surface SG'
            row[74] = 'Surface SG has increased, moved to Scenario 1 as the SLOP is Land only'
        if  row[9] >= 1 and row[10]-row[9] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[71] <> 'Yes':
            row[72] = 1
            row[73] = 'Surface SG'
            row[74] = 'Surface SG has decreased, moved to Scenario 1 as the SLOP is Land only'
        # Scenario 6 - SLOP within Surface SG, EHPZ1 and RSZ where Surface SG has changed
        if  row[9] >= 1 and row[9]-row[10] >= 1 and row[11] < 1 and row[13] >= 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[71] == 'Yes':
            row[72] = 6
            row[73] = 'Surface SG, EHPZ 1 and RSZ'
            row[74] = 'Surface SG has increased'
        if  row[9] >= 1 and row[10]-row[9] >= 1 and row[11] < 1 and row[13] >= 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[71] == 'Yes':
            row[72] = 6
            row[73] = 'Surface SG, EHPZ 1 and RSZ'
            row[74] = 'Surface SG has decreased'
        if  row[9] >= 1 and row[9]-row[10] >= 1 and row[11] < 1 and row[13] >= 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[71] <> 'Yes':
            row[72] = 2
            row[73] = 'Surface SG and EHPZ 1'
            row[74] = 'Surface SG has increased, moved to Scenario 2 as the SLOP is Land only'
        if  row[9] >= 1 and row[10]-row[9] >= 1 and row[11] < 1 and row[13] >= 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[71] <> 'Yes':
            row[72] = 2
            row[73] = 'Surface SG and EHPZ 1'
            row[74] = 'Surface SG has decreased, moved to Scenario 2 as the SLOP is Land only'
        # Scenario 7 - SLOP within Surface SG, EHPZ2 and RSZ where Surface SG has changed
        if  row[9] >= 1 and row[9]-row[10] >= 1 and row[11] < 1 and row[13] < 1 and row[15] >= 1 and row[17] < 1 and row[19] >= 1 and row[71] == 'Yes':
            row[72] = 7
            row[73] = 'Surface SG, EHPZ 2 and RSZ'
            row[74] = 'Surface SG has increased'
        if  row[9] >= 1 and row[10]-row[9] >= 1 and row[11] < 1 and row[13] < 1 and row[15] >= 1 and row[17] < 1 and row[19] >= 1 and row[71] == 'Yes':
            row[72] = 7
            row[73] = 'Surface SG, EHPZ 2 and RSZ'
            row[74] = 'Surface SG has decreased'
        if  row[9] >= 1 and row[9]-row[10] >= 1 and row[11] < 1 and row[13] < 1 and row[15] >= 1 and row[17] < 1 and row[19] >= 1 and row[71] <> 'Yes':
            row[72] = 3
            row[73] = 'Surface SG and EHPZ 2'
            row[74] = 'Surface SG has increased, moved to Scenario 3 as the SLOP is Land only'
        if  row[9] >= 1 and row[10]-row[9] >= 1 and row[11] < 1 and row[13] < 1 and row[15] >= 1 and row[17] < 1 and row[19] >= 1 and row[71] <> 'Yes':
            row[72] = 3
            row[73] = 'Surface SG and EHPZ 2'
            row[74] = 'Surface SG has decreased, moved to Scenario 3 as the SLOP is Land only'
        # Scenario 8 - SLOP within Surface SG, EHPZ3 and RSZ where Surface SG has changed
        if  row[9] >= 1 and row[9]-row[10] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] >= 1 and row[19] >= 1 and row[71] == 'Yes':
            row[72] = 8
            row[73] = 'Surface SG, EHPZ 3 and RSZ'
            row[74] = 'Surface SG has increased'
        if  row[9] >= 1 and row[10]-row[9] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] >= 1 and row[19] >= 1 and row[71] == 'Yes':
            row[72] = 8
            row[73] = 'Surface SG, EHPZ 3 and RSZ'
            row[74] = 'Surface SG has decreased'
        if  row[9] >= 1 and row[9]-row[10] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] >= 1 and row[19] >= 1 and row[71] <> 'Yes':
            row[72] = 4
            row[73] = 'Surface SG and EHPZ 3'
            row[74] = 'Surface SG has increased, moved to Scenario 4 as the SLOP is Land only'
        if  row[9] >= 1 and row[10]-row[9] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] >= 1 and row[19] >= 1 and row[71] <> 'Yes':
            row[72] = 4
            row[73] = 'Surface SG and EHPZ 3'
            row[74] = 'Surface SG has decreased, moved to Scenario 4 as the SLOP is Land only'
        # Scenario 9 - SLOP within EHPZ3
        if  row[9] < 1 and row[13] < 1 and row[15] < 1 and row[17] >= 1 and row[19] < 1:
            row[72] = 9
            row[73] = 'EHPZ 3 only'
        # Scenario 10 - SLOP within EHPZ 3 and RSZ
        if  row[9] < 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] >= 1 and row[19] >= 1 and row[71] == 'Yes':
            row[72] = 10
            row[73] = 'EHPZ 3 and RSZ'
        if  row[9] < 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] >= 1 and row[19] >= 1 and row[71] <> 'Yes':
            row[72] = 9
            row[73] = 'EHPZ 3 only' 
            row[74] = 'Moved to Scenario 9 as the SLOP is Land only'
        # Scenario 11 - SLOP within Surface SG and also in Sub Surface SG 
        if  row[9] >= 1 and row[11] >= 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] < 1:
            row[72] = 11
            row[73] = 'Surface SG and also in Sub Surface SG'
        # Scenario 12 - SLOP was previously within Surface SG and now in Sub Surface SG 
        if  row[10] >= 1 and row[9] < 1 and row[11] >= 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] < 1:
            row[72] = 12
            row[73] = 'Was in Surface SG and now in Sub Surface SG'
        # Scenario 13 - SLOP newly within Sub Surface SG only 
        if  row[9] < 1 and row[12] < 1 and row[11] >= 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] < 1:
            row[72] = 13
            row[73] = 'New to Sub Surface SG only'
        # Scenario 14 - SLOP within Sub Surface SG and RSZ 
        if  row[9] < 1 and row[12] < 1 and row[11] >= 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[71] == 'Yes':
            row[72] = 14
            row[73] = 'In Sub Surface SG and RSZ'
        if  row[9] < 1 and row[12] < 1 and row[11] >= 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[71] <> 'Yes':
            row[72] = 13
            row[73] = 'New to Sub Surface SG only'
            row[74] = 'Moved to Scenario 13 as the SLOP is Land only'
        # Scenario 15 - SLOP was in Surface SG and now in no Zone
        if  row[10] >= 1 and row[9] < 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] < 1:
            row[72] = 15
            row[73] = 'Was in Surface SG and now in no Zone'
        # Scenario 16 - SLOP was in RSZ and now in no Zone
        if  row[20] >= 1 and row[9] < 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] < 1 and row[71] == 'Yes':
            row[72] = 16
            row[73] = 'Was in RSZ and now in no Zone'
        # Scenario 17 - SLOP was in Subsurface SG and now in no Zone
        if  row[12] >= 1 and row[9] < 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] < 1:
            row[72] = 17
            row[73] = 'Was in Sub Surface SG and now in no Zone' 
###=========================================================================================================================================== No change scenarios below
        # Scenario A - SLOP within RSZ with no change
        if  row[9] < 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[19]-row[20] <= 1 and row[20]-row[19] <= 1 and row[19] <> 0 and row[20] <> 0 and row[71] == 'Yes':  
            row[72] = 'A'
            row[73] = 'In RSZ Only'
        if  row[9] < 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[19]-row[20] <= 1 and row[20]-row[19] <= 1 and row[19] <> 0 and row[20] <> 0 and row[71] <> 'Yes':  
            row[72] = 'A'
            row[73] = 'In RSZ Only'
            row[74] = 'In RSZ but no dwelling'
        # Scenario B - SLOP within SubSurface Safeguarding with no change
        if  row[9] < 1 and row[11] >= 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] < 1 and row[11]-row[12] <= 1 and row[12]-row[11] <= 1 and row[11] <> 0 and row[12] <> 0:  
            row[72] = 'B'
            row[73] = 'Remains in Sub Surface SG'
        # Scenario C - SLOP within Sub Surface SG and RSZ with no change
        if  row[9] < 1 and row[11] >= 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[11]-row[12] <= 1 and row[12]-row[11] <= 1 and row[11] <> 0 and row[12] <> 0 and row[71] == 'Yes':  
            row[72] = 'C'
            row[73] = 'Remains in Sub Surface SG and RSZ'
        if  row[9] < 1 and row[11] >= 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[11]-row[12] <= 1 and row[12]-row[11] <= 1 and row[11] <> 0 and row[12] <> 0 and row[71] <> 'Yes':  
            row[72] = 'B'
            row[73] = 'Remains in Sub Surface SG'
            row[74] = 'Moved to Scenario B as the SLOP is Land only'
        # Scenario D - SLOP within EHPZ1 with no change
        if  row[9] < 1 and row[11] < 1 and row[13] >= 1 and row[13]-row[14] <= 1 and row[14]-row[13] <= 1 and row[13] <> 0 and row[14] <> 0  and row[15] < 1 and row[17] < 1 and row[19] < 1:  
            row[72] = 'D'
            row[73] = 'EHPZ 1 only'
        # Scenario E - SLOP within EHPZ1 and RSZ with no change
        if  row[9] < 1 and row[11] < 1 and row[13] >= 1 and row[13]-row[14] <= 1 and row[14]-row[13] <= 1 and row[13] <> 0 and row[14] <> 0 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[71] == 'Yes':  
            row[72] = 'E'
            row[73] = 'EHPZ 1 and RSZ'
        if  row[9] < 1 and row[11] < 1 and row[13] >= 1 and row[13]-row[14] <= 1 and row[14]-row[13] <= 1 and row[13] <> 0 and row[14] <> 0 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[71] <> 'Yes':  
            row[72] = 'D'
            row[73] = 'EHPZ 1 only'
            row[74] = 'Moved to Scenario D as the SLOP is Land only'
        # Scenario F - SLOP within EHPZ2 with no change
        if  row[9] < 1 and row[11] < 1 and row[13] < 1 and row[15] >= 1 and row[15]-row[16] <= 1 and row[16]-row[15] <= 1 and row[15] <> 0 and row[16] <> 0 and row[17] < 1 and row[19] < 1:  
            row[72] = 'F'
            row[73] = 'EHPZ 2 only'
        # Scenario G - SLOP within EHPZ2 and RSZ with no change
        if row[9] < 1 and row[11] < 1 and row[13] < 1 and row[15] >= 1 and row[15]-row[16] <= 1 and row[16]-row[15] <= 1 and row[15] <> 0 and row[16] <> 0 and row[17] < 1 and row[19] >= 1 and row[71] == 'Yes':  
            row[72] = 'G'
            row[73] = 'EHPZ 2 and RSZ'
        if row[9] < 1 and row[11] < 1 and row[13] < 1 and row[15] >= 1 and row[15]-row[16] <= 1 and row[16]-row[15] <= 1 and row[15] <> 0 and row[16] <> 0 and row[17] < 1 and row[19] >= 1 and row[71] <> 'Yes':  
            row[72] = 'F'
            row[73] = 'EHPZ 2 only'
            row[74] = 'Moved to Scenario F as the SLOP is Land only'
        # Scenario H - SLOP within Surface SG with no change
        if  row[9] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] < 1 and row[9]-row[10] <= 1 and row[10]-row[9] <= 1 and row[9] <> 0 and row[10] <> 0:  
            row[72] = 'H'
            row[73] = 'Surface SG only'
        # Scenario I - SLOP within Surface SG and RSZ with no change
        if  row[9] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[9]-row[10] <= 1 and row[10]-row[9] <= 1 and row[9] <> 0 and row[10] <> 0 and row[71] == 'Yes':  
            row[72] = 'I'
            row[73] = 'Surface SG and RSZ'
        if  row[9] >= 1 and row[11] < 1 and row[13] < 1 and row[15] < 1 and row[17] < 1 and row[19] >= 1 and row[9]-row[10] <= 1 and row[10]-row[9] <= 1 and row[9] <> 0 and row[10] <> 0 and row[71] <> 'Yes':  
            row[72] = 'H'
            row[73] = 'Surface SG only'
            row[74] = 'Moved to Scenario H as the SLOP is Land only'
        # Scenario Z - SLOP likely slivers
        if  row[9] < 1 and row[10] < 1 and row[11] < 1 and row[12] < 1 and row[13] < 1 and row[14] >= 1 and row[15] < 1 and row[16] < 1 and row[17] < 1 and row[18] < 1 and row[19] < 1 and row[20] < 1:  
            row[72] = 'Z'
            row[73] = 'Exclude'
            row[74] = 'Intersection with all zones <1sqm, likely slivers'
        cursor.updateRow(row)
print "Scenarios calculated"

#Capture end time of script
print 'Safeguarding finished in: %s\n\n' % (datetime.now() - start)
