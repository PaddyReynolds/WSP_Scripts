import arcpy
from datetime import *

#Capture start time of script
start = datetime.now()
print 'GDD_L3L4: %s\n' % (start)

# Set global variables
arcpy.env.overwriteOutput = True

# Change the workspace to where you would like the Project folder to be saved
workspace = r"C:\Users\ukdxe008\Documents\Python\L3L4_GDD_Script_Work\TestRuns"

# Change the name of the folder to the Project name
projectname = "L3L4_GDD_Script"

# Auto name GDB file
##GDB_FileName = arcpy.CalculateValue_management("AutoGDBName","""import datetime
##now = datetime.datetime.now()
##WeekNum = str(now.isocalendar()[1])
##YearNum = str(now.isocalendar()[0]).strip("20")
##AutoGDBName = "Y" + YearNum + "W" + WeekNum""", "STRING")


#      Create a container folder within the specified workspace containing the folder specified as Project Name above and dated to current date time
createprojectfolder = arcpy.CreateFolder_management(workspace, projectname+"_"+str(datetime.today().strftime('%Y%m%d_%H%M%S')))

# Create required FGDBs for Output, WebGIS storage and Working data
Output = arcpy.CreateFileGDB_management(createprojectfolder,"Output.gdb")
Working = arcpy.CreateFileGDB_management(createprojectfolder,"Working.gdb")
QC_Output = arcpy.CreateFileGDB_management(createprojectfolder,"QC_Output.gdb")

#     Copy XML Schema across to project folder


Select_Template_Feature_class = arcpy.CopyFeatures_management("C:\Users\ukdxe008\Documents\Python\L3L4_GDD_Script_Work\P05_Schema_Templates\HS2-HS2-GI-SPE-000-000017_P05\HS2-HS2-GI-SPE-000-000017_P05.gdb\PRP_ORI_CXXXX_LD_LandAccess_Ply",str(Output)+'\PRP_WSP_2C866_LD_LandAccess_Ply')
Select_Noise_Template_Feature_class = arcpy.CopyFeatures_management("C:\Users\ukdxe008\Documents\Python\L3L4_GDD_Script_Work\TestRuns\NM_tests\P05_Schema_Templates\HS2-HS2-GI-SPE-000-000017_P05\HS2-HS2-GI-SPE-000-000017_P05.gdb\PRP_ORI_CXXXX_LD_LandAccessMonitoring_Ply",str(Output)+"\PRP_ORI_2C866_LD_LandAccessMonitoring_Ply")

#    truncate feature class template

Truncate_Feature_Copy = arcpy.TruncateTable_management(Select_Template_Feature_class)
Truncate_NM_Feature_Copy = arcpy.TruncateTable_management(Select_Noise_Template_Feature_class)

#     Select SDE Variables

AccessLicence_Select = arcpy.Select_analysis("C:\Users\ukdxe008\Documents\Python\L3L4_GDD_Script_Work\Checkout_Leeds\L3L4_KD_20200225.gdb\STATUTORY_PROCESSES\AccessLicences",str(Working)+'\AccessLicence_Select')
HMLR = arcpy.Select_analysis("C:\Users\ukdxe008\Documents\Python\L3L4_GDD_Script_Work\Checkout_Leeds\L3L4_KD_20200225.gdb\STATUTORY_PROCESSES\HMLR_Parcels",str(Working)+'\HMLR_Copy')
LOP = arcpy.Select_analysis("C:\Users\ukdxe008\Documents\Python\L3L4_GDD_Script_Work\Checkout_Leeds\L3L4_KD_20200225.gdb\STATUTORY_PROCESSES\LandOwnershipParcels",str(Working)+"\LOP_Copy")



Select_Licences = arcpy.Select_analysis(AccessLicence_Select,str(Working)+'\L_Numbers',"""LicenceID LIKE 'L%' AND SHAPE_Area >4046.86 AND Status = 'Not Issued' AND Sub_Project IN( 'L3L4' , 'MML' , 'CP2', 'CP2.1' ) OR LicenceID LIKE 'G%' AND SHAPE_Area>4046.86 AND Status = 'Not Issued' AND Sub_Project IN( 'L3L4' , 'MML' , 'CP2', 'CP2.1' ) OR LicenceID LIKE 'L%' AND Status IN( 'Agreed' , 'Refused' , 'Outstanding', 'No Longer Required') AND Sub_Project IN( 'L3L4' , 'MML' , 'CP2', 'CP2.1' ) OR LicenceID LIKE 'G%' AND Status IN( 'Agreed' , 'Refused' , 'Outstanding', 'No Longer Required' ) AND Sub_Project IN( 'L3L4' , 'MML' , 'CP2', 'CP2.1')""")
Select_NM_Licences = arcpy.Select_analysis("C:\Users\ukdxe008\Documents\Python\L3L4_GDD_Script_Work\Data_Export_20200106\L3L4_Data_20200107.gdb\AccessLicences",str(Working)+'\AccessLicence_Select_NM',"""LicenceID LIKE'NL%' AND SHAPE_Area>4046.86 AND Status = 'Not Issued'  AND Sub_Project IN( 'L3L4' , 'MML' , 'CP2' ) OR LicenceID LIKE 'NL%' AND Status IN( 'Agreed' , 'Refused' , 'Outstanding' ) AND Sub_Project IN( 'L3L4' , 'MML' , 'CP2' )""")

Expired_Licence_Codeblock = """if [ExpiryDate] < [HS2_RevDate] Then
val = "Yes"
elseif [ExpiryDate] > [HS2_RevDate] Then
val = "No"
else val = "N/A"
end if"""

#date = datetime.today().strftime('%Y/%m/%D')
Date2 = "2022/01/03"

#    Append template and Access licence selection together

noTest = "NO_TEST"

apendLicence_Into_Template = arcpy.Append_management(Select_Licences,Truncate_Feature_Copy,noTest,"HS2_AssetID \"HS2 Asset ID\" true true false 13 Text 0 0 ,First,#;HS2_SuitabilityCode \"HS2 Suitability Code\" true false false 100 Text 0 0 ,First,#;HS2_Phase \"HS2 Project Phase\" true false false 50 Text 0 0 ,First,#;HS2_DocNum \"HS2 Document Number\" true false false 255 Text 0 0 ,First,#;HS2_DocRev \"HS2 Document Revision\" true false false 5 Text 0 0 ,First,#;HS2_RevDate \"HS2 Revision Date\" true false false 8 Date 0 0 ,First,#;HS2_Layer \"HS2 Layer name\" true false false 255 Text 0 0 ,First,#;HS2_Processor \"HS2 Processor\" true true false 50 Text 0 0 ,First,#;Contract \"Contract\" true false false 6 Text 0 0 ,First,#;Originator \"Originator\" true false false 50 Text 0 0 ,First,#;TitleNum \"Title Number\" true true false 2000 Text 0 0 ,First,#;LicenceNum \"Licence Number\" true true false 50 Text 0 0 ,First,#,%Scratch%\\AccessLicences_Select,LicenceID,-1,-1;Status \"Status\" true false false 50 Text 0 0 ,First,#,%Scratch%\\AccessLicences_Select,Status,-1,-1;ExpiryDate \"Expiry Date\" true true false 8 Date 0 0 ,First,#,%Scratch%\\AccessLicences_Select,ExpiryDate,-1,-1;LicenceType \"Licence Type\" true false false 3 Text 0 0 ,First,#;FullPartialTitle \"FullPartialTitle\" true true false 15 Text 0 0 ,First,#;Expired \"Expired\" true false false 5 Text 0 0 ,First,#;Multipart \"Multipart features\" true false false 5 Text 0 0 ,First,#;HS2_SupDoc \"HS2 Supporting Document\" true true false 255 Text 0 0 ,First,#;Shape_Length \"Shape_Length\" false true true 8 Double 0 0 ,First,#,%Scratch%\\AccessLicences_Select,SHAPE_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0 ,First,#,%Scratch%\\AccessLicences_Select,SHAPE_Area,-1,-1")

print 'Append completed'

joinfield = arcpy.JoinField_management(apendLicence_Into_Template,"SHAPE_Area",Select_Licences,"SHAPE_Area",["LicenceID","Status","ExpiryDate"])
                                         #search cursor

print 'Fields joined based on shape area as drop out in append'

##List = ["HS2_SuitabilityCode",""]
##
##Update_Fields = arcpy.da.UpdateCursor()

Enter_Data_Revision_Number = "P100"

st = ["SC2","N",Date2,"2C866-WSP-GI-GDD-100-000003","2C866","PRP_WSP_2C866_LD_LandAccess_Ply","WSP","Partial","R2",Enter_Data_Revision_Number,"ENV"]

#fields = ["HS2_SuitabilityCode","Multipart","HS2_RevDate","HS2_DocNum","HS2_DocRev","Contract","HS2_Layer","Originator","FullPartialTitle","HS2_Phase"]
with arcpy.da.UpdateCursor(apendLicence_Into_Template, ["HS2_SuitabilityCode","Multipart","HS2_RevDate","HS2_DocNum","Contract","HS2_Layer","Originator","FullPartialTitle","HS2_Phase","HS2_DocRev","LicenceNum","LicenceID","Status","Status_1","ExpiryDate","ExpiryDate_1","LicenceType"]) as cursor:
    for row in cursor:
        row[0] = st[0]
        row[1] = st[1]
        row[2] = st[2]
        row[3] = st[3]
        row[4] = st[4]
        row[5] = st[5]
        row[6] = st[6]
        row[7] = st[7]
        row[8] = st[8]
        row[9] = st[9]
        row[10] = row[11]
        row[12] = row[13]
        row[14] = row[15]
        row[16] = st[10]

        cursor.updateRow(row)

print 'Update cursor completed - domains added'

deleteJoinedfields = arcpy.DeleteField_management(apendLicence_Into_Template,["LicenceID","Status_1","ExpiryDate_1"])

#     deleted joined fields so the data is back to only suitable fields

#    Make Feature data set

MakeFeature_toNull_NonAgreed_ExpiryDates = arcpy.MakeFeatureLayer_management(apendLicence_Into_Template,str(Working)+'\PRP_WSP_2C866_LD_LandAccess_',"","","OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;HS2_AssetID HS2_AssetID VISIBLE NONE;HS2_SuitabilityCode HS2_SuitabilityCode VISIBLE NONE;HS2_Phase HS2_Phase VISIBLE NONE;HS2_DocNum HS2_DocNum VISIBLE NONE;HS2_DocRev HS2_DocRev VISIBLE NONE;HS2_RevDate HS2_RevDate VISIBLE NONE;HS2_Layer HS2_Layer VISIBLE NONE;HS2_Processor HS2_Processor VISIBLE NONE;Contract Contract VISIBLE NONE;Originator Originator VISIBLE NONE;HS2_SupDoc HS2_SupDoc VISIBLE NONE;TitleNum TitleNum VISIBLE NONE;LicenceNum LicenceNum VISIBLE NONE;Status Status VISIBLE NONE;ExpiryDate ExpiryDate VISIBLE NONE;LicenceType LicenceType VISIBLE NONE;FullPartialTitle FullPartialTitle VISIBLE NONE;Expired Expired VISIBLE NONE;Multipart Multipart VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE")

#        Update_Non_Agreed_Licences_to_Null

with arcpy.da.UpdateCursor(MakeFeature_toNull_NonAgreed_ExpiryDates, ['Status','ExpiryDate']) as cursor:
    for row in cursor:
        if (row[0] <> 'Agreed' and row[1] <> None):
            row[1] = None

            cursor.updateRow(row)

print 'update non agreed licences with Null expiry date'

# Update the expiry date field is agreed and no expiry date

#Calculate_Expired = arcpy.CalculateField_management(Clear_Selection_NonAgreed_Licence,"Expired","val","VB",Expired_Licence_Codeblock)

print 'Expired Licences updated'

Intersect_Licences_with_HMLR = arcpy.Intersect_analysis([MakeFeature_toNull_NonAgreed_ExpiryDates,HMLR],str(Working)+'\HMLR_Licence_Inter',"ALL", "", "INPUT")

Repair_Geo_of_intersect = arcpy.RepairGeometry_management(Intersect_Licences_with_HMLR)

Dissolve_HMLR_licence_Inter = arcpy.Dissolve_management(Intersect_Licences_with_HMLR,str(Working)+'\HMLR_Licence_Dissolve',["LicenceNum","HMLR_Title_No"],"","MULTI_PART")

print 'Dissolve HMLR Licence Intersect complete'

print 'Started HMLR Merge process'


Add_HMLR_Merge_Field = arcpy.AddField_management(Dissolve_HMLR_licence_Inter,"HMLR_Merge","TEXT","","","100000")

Delimiter = ','
HMLR_Title_No = 'HMLR_Title_No'

HMLR_Dictionary = {}

lastid = -1

lastvalue = ""
Cur1 = arcpy.SearchCursor(Dissolve_HMLR_licence_Inter,"","","","LicenceNum" +" A;" + HMLR_Title_No +" A")

for row in Cur1:
    id = row.getValue("LicenceNum")
    value = row.getValue(HMLR_Title_No)
    HMLR_Dictionary[id] = value
    if id == lastid:
        value = str(lastvalue) + Delimiter + str(value)
        HMLR_Dictionary[id] = value
    lastid = id
    lastvalue = value
del Cur1, row

# Insert Update cursor to update or delete rows on the specified feature class, shapefile, or table.
cur2 = arcpy.UpdateCursor(Dissolve_HMLR_licence_Inter)
for row in cur2:
    id = row.getValue("LicenceNum")
    row.setValue("HMLR_Merge", HMLR_Dictionary[id])
    cur2.updateRow(row)
del cur2, row

print 'Concatenating HMLR complete'

HMLRdissolve2 = arcpy.Dissolve_management(Dissolve_HMLR_licence_Inter, str(Working)+"\Licence_HMLRDissolveMerge", ["LicenceNum","HMLR_Merge"])

joinConcatenatedHMLR = arcpy.JoinField_management(MakeFeature_toNull_NonAgreed_ExpiryDates, "LicenceNum", HMLRdissolve2, 'LicenceNum', "HMLR_Merge")

Calculate_only_first_2000_characters = arcpy.CalculateField_management(joinConcatenatedHMLR,"HMLR_Merge", "!HMLR_Merge![0:1999]", "PYTHON_9.3")

Update_Title_field = arcpy.CalculateField_management(Calculate_only_first_2000_characters,"TitleNum","""!HMLR_Merge! if !HMLR_Merge! is not None else !TitleNum!""","PYTHON_9.3")

print 'concatenate HMLR Ref complete'

print "HMLR Merge calculated"


Delete_HMLR_MergeFIeld = arcpy.DeleteField_management(Update_Title_field, "HMLR_Merge")

print 'Title number updated with concatenated HMLR values'

print 'Update null title values with U numbers'


Copy_Licence_Without_Title = arcpy.Select_analysis(Delete_HMLR_MergeFIeld,str(Working)+"\Licences_without_Titles")

Intersect_Unique_Parcels_With_LOP = arcpy.Intersect_analysis([Copy_Licence_Without_Title,LOP], str(Working)+"\Unique_Inter_LOP","ALL", "", "INPUT")

print 'intersect LOP and licences without title'

repair_geo = arcpy.RepairGeometry_management(Intersect_Unique_Parcels_With_LOP)

dissolve_LOP_ExternalRef = arcpy.Dissolve_management(repair_geo,str(Working)+"\Dissolve_LOP_Licence_Inter",["ExternalReference","LicenceNum"])

Add_Unique_value = arcpy.AddField_management(dissolve_LOP_ExternalRef,"Unique_Value","TEXT","","","10000")

print "unique fields added and start of concatenating Unique values"

Delimiter = ','
Unique_value = 'Unique_Value'

Uni_V_Dictionary = {}

lastid = -1

lastvalue = ""
Cur4 = arcpy.SearchCursor(dissolve_LOP_ExternalRef,"","","","LicenceNum" +" A;" + Unique_value +" A")

for row in Cur4:
    id = row.getValue("LicenceNum")
    value = row.getValue(Unique_value)
    Uni_V_Dictionary[id] = value
    if id == lastid:
        value = str(lastvalue) + Delimiter + str(value)
        Uni_V_Dictionary[id] = value
    lastid = id
    lastvalue = value
del Cur4, row

# Insert Update cursor to update or delete rows on the specified feature class, shapefile, or table.
cur3 = arcpy.UpdateCursor(dissolve_LOP_ExternalRef)
for row in cur3:
    id = row.getValue("LicenceNum")
    row.setValue("Unique_Value", Uni_V_Dictionary[id])
    cur3.updateRow(row)
del cur3, row


update_uniquevalues = arcpy.CalculateField_management(Add_Unique_value,"Unique_Value","""!ExternalReference!""", "PYTHON_9.3")

print 'concatenated unique values'

dissolve_unique_Values = arcpy.Dissolve_management(Add_Unique_value,str(Working)+"\Dissolve_Unique_V_and_Licences",["Unique_Value","LicenceNum"])

Select_all_Parcels_with_U_Numbers = arcpy.Select_analysis(dissolve_unique_Values,str(Working)+"\All_UNum_Licence","""Unique_Value IS NOT Null""")

print 'Unique value dissolve complete'

join_unique_Fields = arcpy.JoinField_management(Delete_HMLR_MergeFIeld,"LicenceNum",Select_all_Parcels_with_U_Numbers,"LicenceNum","Unique_Value")

Calculate_only_first_Unique_2000_characters = arcpy.CalculateField_management(join_unique_Fields,"Unique_Value", "!Unique_Value![0:1999]", "PYTHON_9.3")

calculate_unique_values_Across = arcpy.CalculateField_management(Delete_HMLR_MergeFIeld,"TitleNum", """!Unique_Value! if !Unique_Value! is not None and !TitleNum! == " " else !TitleNum!""","PYTHON_9.3")


delete_Joined_unique_field = arcpy.DeleteField_management(Delete_HMLR_MergeFIeld,"Unique_Value")

print "Normal Licence GDD completed"



print "Start NM GDD"
   #### Start of NM licence script




Select_NM_Licences = arcpy.Select_analysis("C:\Users\ukdxe008\Documents\Python\L3L4_GDD_Script_Work\Working.gdb\AccessLicence",str(Working)+'\AccessLicence_Select_NM',"""LicenceID LIKE'NL%' AND SHAPE_Area>4046.86 AND Status = 'Not Issued'  AND Sub_Project IN( 'L3L4' , 'MML' , 'CP2' ) OR LicenceID LIKE 'NL%' AND Status IN( 'Agreed' , 'Refused' , 'Outstanding' ) AND Sub_Project IN( 'L3L4' , 'MML' , 'CP2' )""")

#append_NM_in = arcpy.Append_management(Select_NM_Licences, Truncate_Feature_Copy, "NO_TEST", "HS2_AssetID \"HS2 Asset ID\" true true false 13 Text 0 0 ,First,#;HS2_SuitabilityCode \"HS2 Suitability Code\" true false false 100 Text 0 0 ,First,#;HS2_Phase \"HS2 Project Phase\" true false false 50 Text 0 0 ,First,#;HS2_DocNum \"HS2 Document Number\" true false false 50 Text 0 0 ,First,#;HS2_DocRev \"HS2 Document Revision\" true false false 5 Text 0 0 ,First,#;HS2_RevDate \"HS2 Revision Date\" true false false 8 Date 0 0 ,First,#;HS2_Layer \"HS2 Layer name\" true true false 255 Text 0 0 ,First,#;HS2_Processor \"HS2 Processor\" true true false 50 Text 0 0 ,First,#;Contract \"Contract\" true false false 6 Text 0 0 ,First,#;Originator \"Originator\" true false false 50 Text 0 0 ,First,#;HS2_SupDoc \"HS2 Supporting Document\" true true false 255 Text 0 0 ,First,#;TitleNum \"Title Number\" true false false 2000 Text 0 0 ,First,#;LicenceNum \"Licence Number\" true false false 50 Text 0 0 ,First,#,%Scratch%\\Monitoring_Licences,LicenceID,-1,-1;Status \"Status\" true false false 50 Text 0 0 ,First,#,%Scratch%\\Monitoring_Licences,Status,-1,-1;ExpiryDate \"Expiry Date\" true true false 8 Date 0 0 ,First,#,%Scratch%\\Monitoring_Licences,ExpiryDate,-1,-1;MonLicType \"Monitoring Licence Type\" true false false 3 Text 0 0 ,First,#;Expired \"Expired\" true false false 5 Text 0 0 ,First,#;Multipart \"Multipart features\" true false false 5 Text 0 0 ,First,#;Shape_Length \"Shape_Length\" false true true 8 Double 0 0 ,First,#,%Scratch%\\Monitoring_Licences,SHAPE_length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0 ,First,#,%Scratch%\\Monitoring_Licences,SHAPE_area,-1,-1", "")

Append_NM_In = arcpy.Append_management(Select_NM_Licences, Truncate_NM_Feature_Copy, noTest, "HS2_AssetID \"HS2 Asset ID\" true true false 13 Text 0 0 ,First,#;HS2_SuitabilityCode \"HS2 Suitability Code\" true false false 100 Text 0 0 ,First,#;HS2_Phase \"HS2 Project Phase\" true false false 50 Text 0 0 ,First,#;HS2_DocNum \"HS2 Document Number\" true false false 50 Text 0 0 ,First,#;HS2_DocRev \"HS2 Document Revision\" true false false 5 Text 0 0 ,First,#;HS2_RevDate \"HS2 Revision Date\" true false false 8 Date 0 0 ,First,#;HS2_Layer \"HS2 Layer name\" true true false 255 Text 0 0 ,First,#;HS2_Processor \"HS2 Processor\" true true false 50 Text 0 0 ,First,#;Contract \"Contract\" true false false 6 Text 0 0 ,First,#;Originator \"Originator\" true false false 50 Text 0 0 ,First,#;HS2_SupDoc \"HS2 Supporting Document\" true true false 255 Text 0 0 ,First,#;TitleNum \"Title Number\" true false false 2000 Text 0 0 ,First,#;LicenceNum \"Licence Number\" true false false 50 Text 0 0 ,First,#,%Scratch%\\Monitoring_Licences,LicenceID,-1,-1;Status \"Status\" true false false 50 Text 0 0 ,First,#,%Scratch%\\Monitoring_Licences,Status,-1,-1;ExpiryDate \"Expiry Date\" true true false 8 Date 0 0 ,First,#,%Scratch%\\Monitoring_Licences,ExpiryDate,-1,-1;MonLicType \"Monitoring Licence Type\" true false false 3 Text 0 0 ,First,#;Expired \"Expired\" true false false 5 Text 0 0 ,First,#;Multipart \"Multipart features\" true false false 5 Text 0 0 ,First,#;Shape_Length \"Shape_Length\" false true true 8 Double 0 0 ,First,#,%Scratch%\\Monitoring_Licences,SHAPE_length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0 ,First,#,%Scratch%\\Monitoring_Licences,SHAPE_area,-1,-1", "")


print "append worked"

joinfield = arcpy.JoinField_management(Append_NM_In,"SHAPE_Area",Select_NM_Licences,"SHAPE_Area",["LicenceID","Status","ExpiryDate"])
                                         #search cursor



codeblock_for_NM = """def func(dup):
    if "NL" in dup:
        return "NM"
    elif "G" in dup:
        return "GIM"""



List_of_Inputs = ["R2",Date2, "2C866", "N", "WSP", "PRP_WSP_2C866_LD_LandAccessMonitoring_Ply", "2C866-WSP-GI-GDD-100-000003", "SC2", Enter_Data_Revision_Number]

with arcpy.da.UpdateCursor(Append_NM_In, ["HS2_Phase", "HS2_RevDate", "Contract", "Multipart", "Originator", "HS2_Layer", "HS2_DocNum", "HS2_SuitabilityCode", "HS2_DocRev","LicenceNum", "LicenceID","Status","Status_1","ExpiryDate","ExpiryDate_1"]) as cursor:
    for row in cursor:
        row[0] = List_of_Inputs[0]
        row[1] = List_of_Inputs[1]
        row[2] = List_of_Inputs[2]
        row[3] = List_of_Inputs[3]
        row[4] = List_of_Inputs[4]
        row[5] = List_of_Inputs[5]
        row[6] = List_of_Inputs[6]
        row[7] = List_of_Inputs[7]
        row[8] = List_of_Inputs[8]
        row[9]= row[10]
        row[11] = row[12]
        row[13] = row [14]

        cursor.updateRow(row)

print "update cursor worked"

deleteJoinedfields = arcpy.DeleteField_management(Append_NM_In,["LicenceID","Status_1","ExpiryDate_1"])

print "joined fields deleted"


#Select_Non_Agreed_NM = arcpy.Select_Analysis(append_NM_in, str(Working)+"\Select_Non_Agreed_NM", """NOT Status = 'Agreed' AND NOT ExpiryDate IS NULL""")

MakeFeature_Layer_NM =arcpy.MakeFeatureLayer_management(Append_NM_In, str(Working)+"\PRP_ORI_CXXXX_LD_LandAccessMonitoring_Ply", "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;HS2_AssetID HS2_AssetID VISIBLE NONE;HS2_SuitabilityCode HS2_SuitabilityCode VISIBLE NONE;HS2_Phase HS2_Phase VISIBLE NONE;HS2_DocNum HS2_DocNum VISIBLE NONE;HS2_DocRev HS2_DocRev VISIBLE NONE;HS2_RevDate HS2_RevDate VISIBLE NONE;HS2_Layer HS2_Layer VISIBLE NONE;HS2_Processor HS2_Processor VISIBLE NONE;Contract Contract VISIBLE NONE;Originator Originator VISIBLE NONE;HS2_SupDoc HS2_SupDoc VISIBLE NONE;TitleNum TitleNum VISIBLE NONE;LicenceNum LicenceNum VISIBLE NONE;Status Status VISIBLE NONE;ExpiryDate ExpiryDate VISIBLE NONE;LicenceType LicenceType VISIBLE NONE;FullPartialTitle FullPartialTitle VISIBLE NONE;Expired Expired VISIBLE NONE;Multipart Multipart VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE")


Select_NonAgreed_NM = arcpy.SelectLayerByAttribute_management(MakeFeature_Layer_NM,"NEW_SELECTION","NOT Status = 'Agreed' AND NOT ExpiryDate IS NULL")

Calculate_Null_NM = arcpy.CalculateField_management(Select_NonAgreed_NM,"ExpiryDate","null","VB")

Clear_NonAgreed_NM_select = arcpy.SelectLayerByAttribute_management(Calculate_Null_NM,"CLEAR_SELECTION")


print 'calculated expiry dates'

codeblock_for_Expired_field = """if [ExpiryDate] < [HS2_RevDate] Then
val = "Yes"
elseif [ExpiryDate] > [HS2_RevDate] Then
val = "No"
else val = "N/A"
end if"""

calculate_Monitoring_Expired_field = arcpy.CalculateField_management(Clear_NonAgreed_NM_select,"Expired","val","VB", codeblock_for_Expired_field)

print "calculated expired field"



Intersect_NM_Licences_with_HMLR = arcpy.Intersect_analysis([calculate_Monitoring_Expired_field,HMLR],str(Working)+'\HMLR_NM_Licence_Inter',"ALL", "", "INPUT")

Repair_Geo_of_intersect = arcpy.RepairGeometry_management(Intersect_NM_Licences_with_HMLR)

Dissolve_HMLR_NM_licence_Inter = arcpy.Dissolve_management(Intersect_NM_Licences_with_HMLR,str(Working)+'\HMLR_NM_Licence_Dissolve',["LicenceNum","HMLR_Title_No"],"","MULTI_PART")

print 'Dissolve HMLR Licence Intersect complete'

print 'Started HMLR Merge process'


Add_HMLR_Merge_Field = arcpy.AddField_management(Dissolve_HMLR_NM_licence_Inter,"HMLR_Merge","TEXT","","","100000")

Delimiter = ','
HMLR_Title_No = 'HMLR_Title_No'

HMLR_Dictionary = {}

lastid = -1

lastvalue = ""
Cur1 = arcpy.SearchCursor(Dissolve_HMLR_NM_licence_Inter,"","","","LicenceNum" +" A;" + HMLR_Title_No +" A")

for row in Cur1:
    id = row.getValue("LicenceNum")
    value = row.getValue(HMLR_Title_No)
    HMLR_Dictionary[id] = value
    if id == lastid:
        value = str(lastvalue) + Delimiter + str(value)
        HMLR_Dictionary[id] = value
    lastid = id
    lastvalue = value
del Cur1, row

# Insert Update cursor to update or delete rows on the specified feature class, shapefile, or table.
cur2 = arcpy.UpdateCursor(Dissolve_HMLR_NM_licence_Inter)
for row in cur2:
    id = row.getValue("LicenceNum")
    row.setValue("HMLR_Merge", HMLR_Dictionary[id])
    cur2.updateRow(row)
del cur2, row

print "HMLR concatenate worked"



HMLRdissolve3 = arcpy.Dissolve_management(Dissolve_HMLR_NM_licence_Inter, str(Working)+"\NM_Licence_HMLRDissolveMerge", ["LicenceNum","HMLR_Merge"])

joinConcatenatedHMLR = arcpy.JoinField_management(calculate_Monitoring_Expired_field, "LicenceNum", HMLRdissolve3, 'LicenceNum', "HMLR_Merge")

Calculate_only_first_2000_characters = arcpy.CalculateField_management(joinConcatenatedHMLR,"HMLR_Merge", "!HMLR_Merge![0:1999]", "PYTHON_9.3")

Update_Title_field_NM = arcpy.CalculateField_management(Calculate_only_first_2000_characters,"TitleNum","""!HMLR_Merge! if !HMLR_Merge! is not None else !TitleNum!""","PYTHON_9.3")


Delete_HMLR_MergeFIeld_NM = arcpy.DeleteField_management(Update_Title_field_NM, "HMLR_Merge_NM")

print 'Title number updated with concatenated HMLR values'



Intersect_Unique_Parcels_With_LOP = arcpy.Intersect_analysis([Delete_HMLR_MergeFIeld_NM,LOP], str(Working)+"\NM_Unique_Inter_LOP","ALL", "", "INPUT")

print 'intersect LOP and licences without title'

repair_geo = arcpy.RepairGeometry_management(Intersect_Unique_Parcels_With_LOP)

dissolve_LOP_ExternalRef = arcpy.Dissolve_management(repair_geo,str(Working)+"\Dissolve_LOP_NMLicence_Inter",["ExternalReference","LicenceNum"])

Add_Unique_value = arcpy.AddField_management(dissolve_LOP_ExternalRef,"Unique_Value","TEXT","","","10000")

print "unique fields added and start of concatenating Unique values"

Delimiter = ','
Unique_value = 'Unique_Value'

Uni_V_Dictionary = {}

lastid = -1

lastvalue = ""
Cur4 = arcpy.SearchCursor(dissolve_LOP_ExternalRef,"","","","LicenceNum" +" A;" + Unique_value +" A")

for row in Cur4:
    id = row.getValue("LicenceNum")
    value = row.getValue(Unique_value)
    Uni_V_Dictionary[id] = value
    if id == lastid:
        value = str(lastvalue) + Delimiter + str(value)
        Uni_V_Dictionary[id] = value
    lastid = id
    lastvalue = value
del Cur4, row

# Insert Update cursor to update or delete rows on the specified feature class, shapefile, or table.
cur3 = arcpy.UpdateCursor(dissolve_LOP_ExternalRef)
for row in cur3:
    id = row.getValue("LicenceNum")
    row.setValue("Unique_Value", Uni_V_Dictionary[id])
    cur3.updateRow(row)
del cur3, row



updateshit = arcpy.CalculateField_management(Add_Unique_value,"Unique_Value","""!ExternalReference!""", "PYTHON_9.3")

print 'concatenated unique values'

dissolve_unique_Values_NM = arcpy.Dissolve_management(Add_Unique_value,str(Working)+"\Dissolve_Unique_V_and_NMLicences",["Unique_Value","LicenceNum"])

print 'Unique value dissolve complete'

join_unique_Fields = arcpy.JoinField_management(Delete_HMLR_MergeFIeld_NM,"LicenceNum",dissolve_unique_Values_NM,"LicenceNum","Unique_Value")

print 'Join NM Licence with Unique values'

Calculate_only_first_Unique_2000_characters = arcpy.CalculateField_management(join_unique_Fields,"Unique_Value", "!Unique_Value![0:1999]", "PYTHON_9.3")


delete_Joined_unique_field_NM = arcpy.DeleteField_management(Delete_HMLR_MergeFIeld_NM,"Unique_Value")

print 'GDD script complete'

print 'start QC process'

Self_inter_GDD = arcpy.Intersect_analysis(delete_Joined_unique_field,str(QC_Output)+"\Self_Inter_Licences_GDD")

print 'Self intersection of GDD completed'

Select_missing_Expiry_Date = arcpy.Select_analysis(delete_Joined_unique_field,str(QC_Output)+"\Select_Missing_Expiry","""Status = 'Agreed' AND ExpiryDate IS NULL""")

print 'Select all missing expiry dates'



Total_Parcel_Count = [row for row in arcpy.SearchCursor(delete_Joined_unique_field)]

p_count = len(Total_Parcel_Count)

print (p_count)


Multipart_Single =  arcpy.MultipartToSinglepart_management(delete_Joined_unique_field, str(Working)+"\multi_2_Single1" )


Total_Parcel_Count1 = [row for row in arcpy.SearchCursor(Multipart_Single)]

p_count1 = len(Total_Parcel_Count1)

print (p_count1)

if (p_count < p_count1):
    print 'multipart present'
else:
    print 'no multipart'

print 'script complete'
