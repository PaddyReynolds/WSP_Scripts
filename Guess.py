#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     06/12/2019
# Copyright:   (c) UKPXR011 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
        coords = [[i[0],i[1],i[2],i[3]] for i in arcpy.da.SearchCursor(fc,[Page_Number,Y_field,X_field,"OID@"],query)]
        #Sorts everything (- conversts to negative)
        coords.sort( key=lambda k:(round(k[0],decimals),round(k[1],decimals),round(-k[2],decimals)))
        #Pulls ODI
        order = [i[3] for i in coords]
        #Joins sorted list back to original and counts
        d ={k:v for (v,k) in list(enumerate(order))}
        #print(Parish_List)



        k[1]
        K[2] south west  to north east

        -k[1] Northeast to south west
        K[2]


        k[1]
        -K[2] south east to north West

        -k[1] Northwest to south east
        -K[2]