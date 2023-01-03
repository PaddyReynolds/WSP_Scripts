#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     21/09/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import shutil
from arcpy import mapping
import os
#Open/create a folder

laanum = 'A204_009'


file_Path = r'C:\Users\UKPXR011\Desktop\Scripts\Noitce Plans\Test'
newFolder = file_Path + "\\" + laanum
templateMXD = r'C:\Users\UKPXR011\Desktop\Scripts\Noitce Plans\Sch2_Template.mxd'
newMxd = newFolder + "\\" + laanum + ".mxd"
newGDB = laanum + ".gdb"

oldPath = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\Noitce_Plan_Tool\notices\HS2temp_VM.gdb'
newPath =newFolder + "\\" + newGDB

OldVessel = oldPath +'\\'+'NPvessel'
NewVessel = newPath  +'\\'+'NPvessel'

OldExtents = oldPath +'\\'+ 'newnpsextents_Combined'
NewExtents = newPath  +'\\'+'newnpsextents_Combined'


if os.path.isdir(newFolder) is False:
    os.mkdir(newFolder)
    print 'Folder '+ laanum + ' Created'

else:
    print 'Folder Already Exists'

if os.path.isfile(newMxd):
    print 'MXD Already Exists'



else:

    shutil.copy(templateMXD,newMxd)


    print 'MXD created'

if arcpy.Exists(newPath) is False:

    #create GDB
    arcpy.management.CreateFileGDB(newFolder, newGDB)
    arcpy.env.workspace = newPath
    arcpy.env.overwriteOutput = True
    arcpy.CopyFeatures_management(OldVessel, NewVessel)
    arcpy.CopyFeatures_management(OldExtents, NewExtents)
    print 'GDB Created, features copied'

else:

    print 'GDB Already Exists, features overwritten'
    arcpy.env.workspace = newPath
    arcpy.env.overwriteOutput = True
    #Creating new Features
    arcpy.CopyFeatures_management(OldVessel, NewVessel)
    arcpy.CopyFeatures_management(OldExtents, NewExtents)


mxd = arcpy.mapping.MapDocument(newMxd)


for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("DATASOURCE"):
        source = lyr.dataSource
        if 'HS2temp_VM.gdb' in source:
            print 'Made it'
            print lyr
            lyr.findAndReplaceWorkspacePath(oldPath, newPath)

mxd.save()
mxd.dataDrivenPages.refresh()

ddp = mxd.dataDrivenPages

#ddp.exportToPDF((str(newFolder+"//")), "ALL", multiple_files = "PDF_MULTIPLE_FILES_PAGE_NAME")

