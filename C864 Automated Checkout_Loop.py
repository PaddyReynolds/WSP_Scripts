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

#Set this to the local folder to save the checkouts
Checkout_Folder = r'C:\Users\UKPXR011\Desktop\Scratch\Checkouts'

#set this to be the number of checkouts that you want + 1
checkout_Loop = []

for i in checkout_Loop:

    #Change this Name to the current date
    checkout_Name_Date = 'MCR__23102020_'
    Checkout_Full_Name = checkout_Name_Date + str(i)
    arcpy.CreateFolder_management(Checkout_Folder,Checkout_Full_Name)
    desktopPath = Checkout_Folder +'\\' + Checkout_Full_Name
    #Create work space
    #desktopPath = Checkout_Folder + Checkout_Full_Name
    #Save this MXD locally and re point this path
    folders.append(desktopPath)
    print folders
    #Choose Work Database To Run QC Check
    SDE_Geodatabase = r"Database Connections\HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde"
    arcpy.env.workspace = SDE_Geodatabase


    #Check out Parameters
    GDD_Checkout = Checkout_Full_Name + ".gdb"
    Checkoutlocation = desktopPath + "\\" + GDD_Checkout
    WorkFolder = desktopPath

    arcpy.AddMessage('Excel file created & creating checkout')

    arcpy.CreateFileGDB_management(desktopPath, GDD_Checkout)

    #layers_to_Take = 'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES/HS2phase2B.GSS.AccessLicenceAmends';'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES/HS2phase2B.GSS.AccessLicences';'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES/HS2phase2B.GSS.HMLR_Parcels';'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES/HS2phase2B.GSS.LandOwnershipParcelAmends';'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES/HS2phase2B.GSS.LandOwnershipParcels';'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES/HS2phase2B.GSS.Limits';'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES/HS2phase2B.GSS.relAccessLicences_LandOwnership'
    layers_to_Take = 'Database Connections/HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde/HS2phase2B.GSS.STATUTORY_PROCESSES'

    arcpy.CreateReplica_management(layers_to_Take,"CHECK_OUT", Checkoutlocation,Checkout_Full_Name,"FULL", "CHILD_DATA_SENDER", "DO_NOT_ADD", "DO_NOT_REUSE", "GET_RELATED", "", "DO_NOT_USE_ARCHIVING")

    print Checkout_Full_Name + "Completed"

for i in folders:
    dir_name = i
    output_filename = i
    shutil.make_archive(output_filename, 'zip', dir_name)
    zip_file = output_filename +'.zip'
    #Change this to a folder saved centrally so that anyone can access it
    destination = r'\\cormplbrbs1.corp.pbwan.net\Shared\LandAspects\GSS\Admin\Patrick\Transfer\Checkout'
    dest = shutil.move(zip_file, destination)

