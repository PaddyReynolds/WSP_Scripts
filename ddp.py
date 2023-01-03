#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     25/08/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import os

file_Path = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\Python'
laaNum = 'A101_001'
Template_MXD = 'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\Python\Survey_Template.mxd'
newFolder = file_Path + "\\" + laaNum
new_MXD_Temp = newFolder +"\\" + laaNum +".mxd"
print new_MXD_Temp
#new_MXD = arcpy.mapping.MapDocument(new_MXD_Temp)
#print new_MXD

if os.path.isdir(newFolder) is False:
    os.mkdir(newFolder)
else:
    print('Folder already exists')



#Open the MXD
mxd = arcpy.mapping.MapDocument(Template_MXD)
mxd.saveACopy(newFolder +'\\' + laaNum + ".mxd")

#lyt.mapSeries.refresh().
#Save the MXD with the LAA Name
 #Where to save


#Refresh DDP


#Export all pages
    #Where to export