#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     06/01/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
from arcpy import env
from arcpy import mapping
import os
import shutil
import datetime
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

arcpy.env.overwriteOutput = True
Lnumbers = []
#Date
now = datetime.datetime.now()
Date = now.strftime("%Y%m%d%H%M")
startTime = datetime.datetime.now()
folders= []
'''
limit_Layer = r"Database Connections\HS2-Phase2B-Leeds-L3L4-Lot3-GSS.sde\ACCESSLICENCES_H1"

arcpy.AddMessage("Trying")
with arcpy.da.SearchCursor(limit_Layer,['LicenceID']) as cursor:
    for row in cursor:
        Lnumbers.append(str(row[0]))

arcpy.AddMessage("Done")

Lnumbers = list(dict.fromkeys(Lnumbers))
Lnumbers.sort()


LnumbersRange =  list("L" + str(i) for i in list(range(1, 90000)))
Lnumbers = [x for x in LnumbersRange if x not in Lnumbers]

Available_Lnumbs = []

for L in Lnumbers:
    Available_Lnumbs.append(L)
'''
Checkout_Folder = r'C:\Users\UKPXR011\Desktop\Scratch\Checkouts'

checkout_Loop = [1,2]

for i in checkout_Loop:

    checkout_Name_Date = 'L3L4_SG_07082020_PR_'
    Checkout_Full_Name = checkout_Name_Date + str(i)
    arcpy.CreateFolder_management(Checkout_Folder,Checkout_Full_Name)
    desktopPath = Checkout_Folder +'\\' + Checkout_Full_Name
    folders.append(desktopPath)
    #Create work space
    #desktopPath = Checkout_Folder + Checkout_Full_Name
    MXD_to_Copy = r"C:\Users\UKPXR011\Desktop\Scratch\Checkouts\MXD_Copy.mxd"
    Foldername = 'AmendsFolder_' + str(Date)
    MXD_Copy_Name = str(desktopPath) + "\\" + Foldername + "\\" + "MXD_Copy.mxd"
    #Choose Work Database To Run QC Check
    SDE_Geodatabase = r"Database Connections\HS2-Phase2B-Leeds-L3L4-Lot3-GSS.sde"
    arcpy.env.workspace = SDE_Geodatabase
    Folder_Location = desktopPath + "\\" + Foldername

    #Check out Parameters
    GDD_Checkout = Checkout_Full_Name + ".gdb"
    Checkoutlocation = Folder_Location + "\\" + GDD_Checkout
    WorkFolder = desktopPath
    workGDB = desktopPath +"\\Historical.gdb"

    #Create folder for storing amends and copying mxd
    arcpy.CreateFolder_management(desktopPath,Foldername)
    arcpy.Copy_management(MXD_to_Copy,MXD_Copy_Name)

    targetXL = desktopPath + "\\" + Foldername + "\\" + "AvailableLNum_" + str(Date) + ".xlsx"
    '''
    arcpy.AddMessage('Writing not used l numbers list to folder')

    df = pd.DataFrame(Available_Lnumbs)

    writer = ExcelWriter(targetXL, engine='xlsxwriter')
    df.to_excel(writer,index=False,sheet_name ='AvailableLNums')
    workbook = writer.book
    worksheet = writer.sheets['AvailableLNums']
    format1 = workbook.add_format({'num_format': '#,##0.00'})
    worksheet.set_column('A:A', 28, format1)
    writer.save()
    '''
    arcpy.AddMessage('Excel file created & creating checkout')

    arcpy.CreateFileGDB_management(Folder_Location, GDD_Checkout)

    #layers_to_Take = 'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES/HS2phase2B.GSS.AccessLicenceAmends';'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES/HS2phase2B.GSS.AccessLicences';'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES/HS2phase2B.GSS.HMLR_Parcels';'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES/HS2phase2B.GSS.LandOwnershipParcelAmends';'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES/HS2phase2B.GSS.LandOwnershipParcels';'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES/HS2phase2B.GSS.Limits';'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES/HS2phase2B.GSS.relAccessLicences_LandOwnership'
    layers_to_Take = 'Database Connections\HS2-Phase2B-Leeds-L3L4-Lot3-GSS.sde/HS2phase2B_WSP.GSS.STATUTORY_PROCESSES'

    arcpy.CreateReplica_management(layers_to_Take,"CHECK_OUT", Checkoutlocation,Checkout_Full_Name,"FULL", "CHILD_DATA_SENDER", "DO_NOT_ADD", "DO_NOT_REUSE", "GET_RELATED", "", "DO_NOT_USE_ARCHIVING")

    arcpy.AddMessage('CheckOut complete now copying MXD to folder')

    try:
        arcpy.Copy_management(MXD_to_Copy,MXD_Copy_Name)
        arcpy.AddMessage('MXD successfully copied')
    except:
        arcpy.AddMessage('error in copying MXD')

    arcpy.AddMessage('replacing pathways of copied MXD to check out')

    mxd = mapping.MapDocument(MXD_Copy_Name)
    lyrs = mapping.ListLayers(mxd)
    new_Path = Checkoutlocation

    #replace pathways of old SDE data from amend to new check out

    for lyr in arcpy.mapping.ListLayers(mxd):
        if lyr.supports("DATASOURCE"):
            source = lyr.dataSource
            Old = lyr.workspacePath
            if 'STATUTORY_PROCESSES' in source:
                lyr.findAndReplaceWorkspacePath(Old, new_Path, False)
                print lyr.dataSource
    mxd.save()

    print Checkout_Full_Name + "Completed"


folders.sort()

for i in folders:
    dir_name = i
    output_filename = i
    shutil.make_archive(output_filename, 'zip', dir_name)
    zip_file = output_filename +'.zip'
    destination = r'\\cormplbrbs1.corp.pbwan.net\Shared\LandAspects\GSS\Admin\Patrick\Transfer\Checkout'
    dest = shutil.move(zip_file, destination)

