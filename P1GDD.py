#local

#UKVXM600
# v 2.6 / October 2019
#_____SCRIPT_______________________

# preliminary statements


import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r'C:\Users\UKPXR011\Desktop\Current Work\P1\GDD\GDBtemp.gdb'

LAP = r'C:\Users\UKPXR011\Desktop\Current Work\P1\GDD\Checkout\GDD_W49.gdb\LAP\LAPs'
LAAs = r'C:\Users\UKPXR011\Desktop\Current Work\P1\GDD\Checkout\GDD_W49.gdb\LAAFLAB\LAAs'
LAASHEET = r'C:\Users\UKPXR011\Desktop\Current Work\P1\GDD\Checkout\GDD_W49.gdb\LAAFLAB\LAA_Spreadsheet'
CLRSHEET = r'C:\Users\UKPXR011\Desktop\Current Work\P1\GDD\Checkout\GDD_W49.gdb\CLR\CLRsSpreadsheet'
#CLRSHEET =r'Database Connections\HS2.sde\HS2Phase1_PRA.GSS.CLR\HS2Phase1_PRA.GSS.CLRsSpreadsheet'


WORKLAYER= r'C:\Users\UKPXR011\Desktop\Current Work\P1\GDD\GDBtemp.gdb\Worklayer_LAPS'
WLAAs = r'C:\Users\UKPXR011\Desktop\Current Work\P1\GDD\GDBtemp.gdb\Worklayer_LAAs'
ROWS= r'C:\Users\UKPXR011\Desktop\Current Work\P1\GDD\GDBtemp.gdb\NProws'

#_____PARAMS________

outputfc = r'C:\Users\UKPXR011\Desktop\Current Work\P1\GDD\P1GDD.gdb\tempLAA'
outputex = r'C:\Users\UKPXR011\Desktop\Current Work\P1\GDD\P1GDD.gdb\tempLAP'
vers = "420"
outputgvd = r'C:\Users\UKPXR011\Desktop\Current Work\P1\GDD\P1GDD.gdb\TempGVD'
version = "'{0}'" . format(vers)



#_____FUNCTION DEFINITION________



def add_date():
	import time
	return time.strftime("%d/%m/%Y")
dat = add_date()
date = "'{0}'" . format (dat)



#_____BODY_______________________

arcpy.AddMessage("Deleting previous records")
arcpy.DeleteRows_management(WORKLAYER)
arcpy.DeleteRows_management(WLAAs)

#_____LAPs_______________________

# calcultating the LAP values
arcpy.AddMessage("Processing LAPs")
arcpy.MakeFeatureLayer_management(LAP,"LAP1")
query="LAPStatus IN('WIP','FIN') AND LAAType <> 'SoR'"
arcpy.SelectLayerByAttribute_management("LAP1","NEW_SELECTION",query)
arcpy.Append_management("LAP1", WORKLAYER,"NO_TEST")




# calculating attributes
arcpy.CalculateField_management(WORKLAYER,"Multipart", "!shape.partCount!","PYTHON_9.3")
arcpy.CalculateField_management(WORKLAYER,"HS2_SuitabilityCode","'SC2'","PYTHON_9.3")
arcpy.CalculateField_management(WORKLAYER,"HS2_Phase","'R1'","PYTHON_9.3")
arcpy.CalculateField_management(WORKLAYER,"HS2_DocNum","'1LR02-MCL-GI-GDD-C000-000001'","PYTHON_9.3")
arcpy.CalculateField_management(WORKLAYER,"HS2_DocRev",version,"PYTHON_9.3")
arcpy.CalculateField_management(WORKLAYER,"HS2_RevDate",date,"PYTHON_9.3")
arcpy.CalculateField_management(WORKLAYER,"Contract","'1LR02'","PYTHON_9.3")
arcpy.CalculateField_management(WORKLAYER,"Originator","'MCL'","PYTHON_9.3")
arcpy.CalculateField_management(WORKLAYER,"NumOnPlan","!LAPID!","PYTHON_9.3")
arcpy.CalculateField_management(WORKLAYER,"LAPType","'LOP'","PYTHON_9.3")




# adding "LAP" string to the LAPID
arcpy.AddMessage("Adding LAP string")
string= "'LAP'"
exp="{0}+!LAPID!".format(string)
arcpy.CalculateField_management(WORKLAYER,"LAPID",exp,"PYTHON_9.3")



arcpy.AddMessage("Adding CLR info")
arcpy.MakeFeatureLayer_management(LAASHEET,"Laa_sheet")
arcpy.MakeFeatureLayer_management(WORKLAYER,"Work")
arcpy.AddJoin_management("Work","LAAID","Laa_sheet","LAAID","KEEP_ALL")
arcpy.CalculateField_management("Work","CRID","!LAA_Spreadsheet.CRID!","PYTHON_9.3")
arcpy.CalculateField_management("Work","LAAName","!LAA_Spreadsheet.LAAName!","PYTHON_9.3")
arcpy.RemoveJoin_management("Work")




# removing EXPIRED S2 LAPs
arcpy.AddMessage("Removing expired S2s")
arcpy.AddJoin_management("Work","LAAID",LAAs,"LAAID")
query = "LAAs.DaysLeft < 0"
arcpy.SelectLayerByAttribute_management("Work","NEW_SELECTION",query)
arcpy.DeleteFeatures_management("Work")
arcpy.SelectLayerByAttribute_management("Work","CLEAR_SELECTION")
arcpy.RemoveJoin_management("Work")




# saving
arcpy.AddMessage("Saving...")
arcpy.SaveToLayerFile_management("Work",WORKLAYER)
arcpy.RepairGeometry_management(WORKLAYER)


#_____LAAs_______________________


# saving, correcting and creating the LAAs

arcpy.Dissolve_management(WORKLAYER,WLAAs,["LAAID","LRType"])


# creating fields for the LAA attributes
arcpy.AddMessage("Processing LAAs")
arcpy.AddField_management(WLAAs,"Multipart","TEXT")
arcpy.AddField_management(WLAAs,"HS2_SuitabilityCode","TEXT")
arcpy.AddField_management(WLAAs,"HS2_Phase","TEXT")
arcpy.AddField_management(WLAAs,"HS2_DocNum","TEXT")
arcpy.AddField_management(WLAAs,"HS2_DocRev","TEXT")
arcpy.AddField_management(WLAAs,"HS2_RevDate","TEXT")
arcpy.AddField_management(WLAAs,"Contract","TEXT")
arcpy.AddField_management(WLAAs,"Originator","TEXT")
arcpy.AddField_management(WLAAs,"LAAName","TEXT")
arcpy.AddField_management(WLAAs,"LAAStatus","TEXT")
arcpy.AddField_management(WLAAs,"DescUse","TEXT")
arcpy.AddField_management(WLAAs,"CRID","TEXT")


# calculating LAA attributes
arcpy.CalculateField_management(WLAAs,"Multipart", "!Shape.PartCount!","PYTHON_9.3")
arcpy.CalculateField_management(WLAAs,"HS2_SuitabilityCode","'SC2'","PYTHON_9.3")
arcpy.CalculateField_management(WLAAs,"HS2_Phase","'R1'","PYTHON_9.3")
arcpy.CalculateField_management(WLAAs,"HS2_DocNum","'1LR02-MCL-GI-GDD-C000-000001'","PYTHON_9.3")
arcpy.CalculateField_management(WLAAs,"HS2_DocRev",version,"PYTHON_9.3")
arcpy.CalculateField_management(WLAAs,"HS2_RevDate",date,"PYTHON_9.3")
arcpy.CalculateField_management(WLAAs,"Contract","'1LR02'","PYTHON_9.3")
arcpy.CalculateField_management(WLAAs,"Originator","'MCL'","PYTHON_9.3")


# calculating LAA names, CRIDs
arcpy.AddMessage("Getting LAA names")
arcpy.MakeFeatureLayer_management(WLAAs,"Laas_temp")
arcpy.AddJoin_management("Laas_temp","LAAID","Laa_sheet","LAAID","KEEP_ALL")
arcpy.CalculateField_management("Laas_temp","LAAName","!LAA_Spreadsheet.LAAName!","PYTHON_9.3")
arcpy.CalculateField_management("Laas_temp","CRID","!LAA_Spreadsheet.CRID!","PYTHON_9.3")
arcpy.RemoveJoin_management("Laas_temp")
arcpy.CalculateField_management("Laas_temp","Multipart","!Shape.PartCount!","PYTHON_9.3")


# calculating LAA Status
arcpy.AddJoin_management("Laas_temp","LAAID",WORKLAYER,"LAAID","KEEP_COMMON")
arcpy.CalculateField_management("Laas_temp","LAAStatus","!Worklayer_LAPS.LAPStatus!","PYTHON_9.3")
arcpy.CalculateField_management("Laas_temp","DescUse","!Worklayer_LAPS.LAPDesc!","PYTHON_9.3")
arcpy.RemoveJoin_management("Laas_temp")


# calculating multiparts
clause = "Multipart = '1'"
arcpy.SelectLayerByAttribute_management("Laas_temp","NEW_SELECTION",clause)
arcpy.CalculateField_management("Laas_temp","Multipart","'N'","PYTHON_9.3")

arcpy.SelectLayerByAttribute_management("Laas_temp","SWITCH_SELECTION")
arcpy.CalculateField_management("Laas_temp","Multipart","'Y'","PYTHON_9.3")
arcpy.SelectLayerByAttribute_management("Laas_temp","CLEAR_SELECTION")

# saving feature layer
arcpy.SaveToLayerFile_management("Laas_temp",WLAAs)
arcpy.RepairGeometry_management(WLAAs)



#_____GVDs_______________________


# finding PERM LAAs and exporting to new feature
arcpy.AddMessage("Finding GVDs...")
clause = "LRType = 'PERM'"
arcpy.SelectLayerByAttribute_management("Laas_temp","NEW_SELECTION",clause)
arcpy.CopyFeatures_management("Laas_temp", outputgvd)

# adding fields
arcpy.AddField_management(outputgvd,"GVDNumber","SHORT")
arcpy.AddField_management(outputgvd,"GVDStatus","TEXT")
arcpy.AddField_management(outputgvd,"DatePre","DATE")
arcpy.AddField_management(outputgvd,"DateExec","DATE")
arcpy.AddField_management(outputgvd,"NoticeType","TEXT")
arcpy.AddField_management(outputgvd,"LEN","SHORT")

# calculating fields
arcpy.AddMessage("Finding GVD information...")
arcpy.MakeFeatureLayer_management(outputgvd,"GVDlayer")
arcpy.AddJoin_management("GVDlayer","LAAID",ROWS,"LAA_ID")

arcpy.CalculateField_management("GVDlayer","tempGVD.GVDNumber","!NProws.GVD_Number!","PYTHON_9.3")
arcpy.CalculateField_management("GVDlayer","tempGVD.LEN","len(!tempGVD.LAAID!)","PYTHON_9.3")
arcpy.CalculateField_management("GVDlayer","tempGVD.GVDStatus","'PR'","PYTHON_9.3")

# calculating Executed values
arcpy.AddMessage("Finding executed GVDs...")
query = "NProws.GVD_Execution_Date >= '01/01/2001'"
arcpy.SelectLayerByAttribute_management("GVDlayer","NEW_SELECTION",query)
arcpy.CalculateField_management("GVDlayer","tempGVD.GVDStatus","'EX'","PYTHON_9.3")
arcpy.CalculateField_management("GVDlayer","tempGVD.DateExec","!NProws.GVD_Execution_Date!","PYTHON_9.3")
arcpy.SelectLayerByAttribute_management("GVDlayer","CLEAR_SELECTION")

# calculating Preliminary values
arcpy.AddMessage("Finding preliminary GVDs...")
query = "tempGVD.GVDStatus = 'PR'"
arcpy.SelectLayerByAttribute_management("GVDlayer","NEW_SELECTION",query)
arcpy.CalculateField_management("GVDlayer","tempGVD.DatePre","!NProws.Actual_Date_of_Service__Notice_Served_!","PYTHON_9.3")
arcpy.SelectLayerByAttribute_management("GVDlayer","CLEAR_SELECTION")

arcpy.RemoveJoin_management("GVDlayer")


#calculating notice types
arcpy.AddMessage("Calculating notice types...")
arcpy.AddJoin_management("GVDlayer","LAAID",LAAs,"LAAID")

query="LAAs.NoticeType= 'GPN'"
arcpy.SelectLayerByAttribute_management("GVDlayer","NEW_SELECTION",query)
arcpy.CalculateField_management("GVDlayer","tempGVD.NoticeType","'GPN'","PYTHON_9.3")
arcpy.SelectLayerByAttribute_management("GVDlayer","CLEAR_SELECTION")

query="LAAs.NoticeType= 'GVD'"
arcpy.SelectLayerByAttribute_management("GVDlayer","NEW_SELECTION",query)
arcpy.CalculateField_management("GVDlayer","tempGVD.NoticeType","'GVD'","PYTHON_9.3")
arcpy.SelectLayerByAttribute_management("GVDlayer","CLEAR_SELECTION")

#query="LAAs.NoticeType= 'GVB'"
#arcpy.SelectLayerByAttribute_management("GVDlayer","NEW_SELECTION",query)
#arcpy.CalculateField_management("GVDlayer","tempGVD.NoticeType","'GVB'","PYTHON_9.3")
#arcpy.SelectLayerByAttribute_management("GVDlayer","CLEAR_SELECTION")


arcpy.RemoveJoin_management("GVDlayer")

# saving feature class
arcpy.SaveToLayerFile_management("GVDlayer",outputgvd)


# saving final outputs
arcpy.AddMessage("Almost there...")
arcpy.CopyFeatures_management (WORKLAYER, outputex)
arcpy.CopyFeatures_management (WLAAs, outputfc)
































