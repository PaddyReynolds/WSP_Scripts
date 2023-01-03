# Leeds Stats script

import arcpy
from datetime import *

#Capture start time of script
start = datetime.now()
print 'Safeguarding Started: %s\n' % (start)

# Set global variables
arcpy.env.overwriteOutput = True

# Change the workspace to where you would like the Project folder to be saved
workspace = r"C:\Users\UKPXR011\Desktop\Stats\Stats_111219"

# Change the name of the folder to the Project name
projectname = "L3L4_Stats_Limits"

# Create a container folder within the specified workspace containing the folder specified as Project Name above and dated to current date time
createprojectfolder = arcpy.CreateFolder_management(workspace, projectname+"_"+str(datetime.today().strftime('%Y%m%d_%H%M%S')))

# Create required FGDBs for Output, WebGIS storage and Working data
Output = arcpy.CreateFileGDB_management(createprojectfolder,"Output")
Working = arcpy.CreateFileGDB_management(createprojectfolder,"Working")

#Working = r"C:\Users\ukdxe008\Documents\Python\Dave_Tests\HS2A_Safeguarding_2019_20191107_091135\Working.gdb"

#List of variables
AccessLicence = r"C:\Users\UKPXR011\Desktop\Stats\Scratch.gdb\AccessLicence"
Limits = r"C:\Users\UKPXR011\Desktop\Stats\Scratch.gdb\Limits"

Create_CP2_1_250_Limits = arcpy.Select_analysis(Limits,str(Working)+"\CP2_1_Limits","""LimitDescription = 'Consolidated Construction Boundary CP02.1 + 250m'""")

Create_Enitre_Licence_Coverage_L3L4_Limits = arcpy.Select_analysis(Limits,str(Working)+"\Enitre_Licence_L3L4_Limits","""LimitDescription = 'Entire Licence Coverage (L3 L4)'""")

Create_Enitre_Licence_Coverage_MML_Limits = arcpy.Select_analysis(Limits,str(Working)+"\Enitre_Licence_MML_Limits","""LimitDescription = 'Entire Licence Coverage (only MML)'""")

Create_Enitre_Licence_Coverage_CP2_Limits = arcpy.Select_analysis(Limits,str(Working)+"\Enitre_Licence_CP2_Limits","""LimitDescription = 'Consolidated Construction Boundary CP02'""")

Create_Enitre_Licence_Coverage_CP2_1_Limits = arcpy.Select_analysis(Limits,str(Working)+"\Enitre_Licence_CP2_1_Limits","""LimitDescription = 'Consolidated Construction Boundary CP02.1 v2'""")

Create_Enitre_Licence_Coverage_CP3_Limits = arcpy.Select_analysis(Limits,str(Working)+"\Enitre_Licence_CP3_Limits","""LimitDescription = 'Consolidated Construction Boundary CP03'""")

expression = """AgreedExpired( !Status!, !ExpiryDate!)"""

Codeblock = """import datetime
def AgreedExpired(Status,ExpiryDate):

    if (Status == 'Agreed' and ExpiryDate is None):
        return "Agreed Not Expired"

    elif (Status == 'Agreed' and datetime.datetime.strptime(ExpiryDate, '%d/%m/%Y') <= datetime.datetime.now()):
        return "Agreed Expired"

    elif (Status == 'Agreed' and datetime.datetime.strptime(ExpiryDate, '%d/%m/%Y') >= datetime.datetime.now()):
        return "Agreed Not Expired"

    else:
        return Status"""

print 'Variables run'

Select_AccessLicence_data = arcpy.Select_analysis(AccessLicence,str(Working)+"\WorkingAccessLicence")

Calculate_Argeed_Expired = arcpy.CalculateField_management(Select_AccessLicence_data,"Status",expression,"Python_9.3",Codeblock)

print 'Calc Agreed Expired Complete'

print 'Run Intersect, Add field and Calculate field for CP2_1_buff layer'

Intersect_Licence_With_CP2_1_250 = arcpy.Intersect_analysis([Create_CP2_1_250_Limits,Select_AccessLicence_data], str(Working)+"\CP2_1_250_EAA_Inter", "ALL", "", "INPUT")

Add_In_CP2_1_250_Field = arcpy.AddField_management(Intersect_Licence_With_CP2_1_250,"In_CP2_1_250_Limits_Int","Short")

calculate_CP2_1_250_field = arcpy.CalculateField_management(Add_In_CP2_1_250_Field,"In_CP2_1_250_Limits_Int","1","PYTHON_9.3")

print 'Run Intersect, Add field and Calculate field for L3L4 layer'

Intersect_Licence_With_L3L4 = arcpy.Intersect_analysis([Create_Enitre_Licence_Coverage_L3L4_Limits,Select_AccessLicence_data], str(Working)+"\L3L4_EAA_Inter", "ALL", "", "INPUT")

Add_Int_L3L4_Field = arcpy.AddField_management(Intersect_Licence_With_L3L4,"In_L3L4_Limits_Int","Short")

calculate_L3L4_field = arcpy.CalculateField_management(Add_Int_L3L4_Field,"In_L3L4_Limits_Int","1","PYTHON_9.3")

print 'L3L4 Full worked'

print 'Run Intersect, Add field and Calculate field for MML layer'

Intersect_Licence_With_MML = arcpy.Intersect_analysis([Create_Enitre_Licence_Coverage_MML_Limits,Select_AccessLicence_data], str(Working)+"\MML_EAA_Inter", "ALL", "", "INPUT")

Add_Int_MML_Field = arcpy.AddField_management(Intersect_Licence_With_MML,"In_MML_Limits_Int","Short")

calculate_MML_field = arcpy.CalculateField_management(Add_Int_MML_Field,"In_MML_Limits_Int","1","PYTHON_9.3")

print 'Run Intersect, Add field and Calculate field for CP2 layer'

Intersect_Licence_With_CP2 = arcpy.Intersect_analysis([Create_Enitre_Licence_Coverage_CP2_Limits,Select_AccessLicence_data], str(Working)+"\CP2_EAA_Inter", "ALL", "", "INPUT")

Add_Int_CP2_Field = arcpy.AddField_management(Intersect_Licence_With_CP2,"In_CP2_Limits_Int","Short")

calculate_CP2_field = arcpy.CalculateField_management(Add_Int_CP2_Field,"In_CP2_Limits_Int","1","PYTHON_9.3")

print 'Run Intersect, Add field and Calculate field for CP2_1 layer'

Intersect_Licence_With_CP2_1 = arcpy.Intersect_analysis([Create_Enitre_Licence_Coverage_CP2_1_Limits,Select_AccessLicence_data], str(Working)+"\CP2_1_EAA_Inter", "ALL", "", "INPUT")

Add_Int_CP2_1_Field = arcpy.AddField_management(Intersect_Licence_With_CP2_1,"In_CP2_1_Limits_Int","Short")

calculate_CP2_1_field = arcpy.CalculateField_management(Add_Int_CP2_1_Field,"In_CP2_1_Limits_Int","1","PYTHON_9.3")

print 'Running Intersect, Add field and Calculate field for CP3 layer'

Intersect_Licence_With_CP3 = arcpy.Intersect_analysis([Create_Enitre_Licence_Coverage_CP3_Limits,Select_AccessLicence_data], str(Working)+"\CP3_EAA_Inter", "ALL", "", "INPUT")

Add_Int_CP3_Field = arcpy.AddField_management(Intersect_Licence_With_CP3,"In_CP3_Limits_Int","Short")

calculate_CP3_field = arcpy.CalculateField_management(Add_Int_CP3_Field,"In_CP3_Limits_Int","1","PYTHON_9.3")


print 'Intersects, add fields and calcs comlpete for MML,L3L4,CP2_250,CP2,CP2_1v2'


join_CP2_1_250_to_AccessLicences = arcpy.JoinField_management(Select_AccessLicence_data,"LicenceID",calculate_CP2_1_250_field,"LicenceID","In_CP2_1_250_Limits_Int")
join_L3L4_to_AccessLicences = arcpy.JoinField_management(Select_AccessLicence_data,"LicenceID",calculate_L3L4_field,"LicenceID","In_L3L4_Limits_Int")
join_MML_to_AccessLicences = arcpy.JoinField_management(Select_AccessLicence_data,"LicenceID",calculate_MML_field,"LicenceID","In_MML_Limits_Int")
join_CP2_to_AccessLicences = arcpy.JoinField_management(Select_AccessLicence_data,"LicenceID",calculate_CP2_field,"LicenceID","In_CP2_Limits_Int")
join_CP2_1_to_AccessLicences = arcpy.JoinField_management(Select_AccessLicence_data,"LicenceID",calculate_CP2_1_field,"LicenceID","In_CP2_1_Limits_Int")
join_CP2_3_to_AccessLicences = arcpy.JoinField_management(Select_AccessLicence_data,"LicenceID",calculate_CP3_field,"LicenceID","In_CP3_Limits_Int")


print 'Join fields complete'

#Add_Limits_Define = arcpy.AddField_management(Select_AccessLicence_data,"In_Limits","TEXT")
Add_CP2_1_250_Limits_Define = arcpy.AddField_management(Select_AccessLicence_data,"In_CP2_1_250_Limits","TEXT")
Add_L3L4_Limits_Define = arcpy.AddField_management(Select_AccessLicence_data,"In_L3L4_Limits","TEXT")
Add_MML_Limits_Define = arcpy.AddField_management(Select_AccessLicence_data,"In_MML_Limits","TEXT")
Add_CP2_Limits_Define = arcpy.AddField_management(Select_AccessLicence_data,"In_CP2_Limits","TEXT")
Add_CP2_1_Limits_Define = arcpy.AddField_management(Select_AccessLicence_data,"In_CP2_1_Limits","TEXT")
Add_CP3_Limits_Define = arcpy.AddField_management(Select_AccessLicence_data,"In_CP3_Limits","TEXT")

# calculate what parcels are in what limits


##with arcpy.da.UpdateCursor(Select_AccessLicence_data,["In_CP2_1_250_Limits","In_L3L4_Limits","In_MML_Limits","In_CP2_Limits","In_CP2_1_Limits","In_CP3_Limits","In_MML_Limits_Int","In_L3L4_Limits_Int","In_CP2_1_250_Limits_Int","In_CP2_Limits_Int","In_CP2_1_Limits_Int","In_CP3_Limits_Int"]) as cursor:
##    for row in cursor:
##        if (row[8] == 1):
##            row[0] = "In CP2.1 250m Limits"
##        if (row[7] == 1):
##            row[1] = "In L3L4 Limits"
##        if (row[6] == 1):
##            row[2] = "In MML Limits"
##        if (row[9] == 1):
##            row[3] = "In CP2 Limits"
##        if (row[10] == 1):
##            row[4] = "In CP2.1v2 Limits"
##        if (row[11] == 1):
##            row[5] = "In CP3 Limits"
##
##        cursor.updateRow(row)
##print 'update cursor complete'


# Select out all limits by stats (Not issues over 1 acre etc)

Select_CP2_1_250_Status_Areas = arcpy.Select_analysis(Select_AccessLicence_data,str(Working)+"\Select_CP2_1_250_Areas","""In_CP2_1_250_Limits_Int = 1 AND Status = 'Not Issued' AND SHAPE_Area > 4046.68 OR In_CP2_1_250_Limits_Int = 1 AND Status IN( 'Outstanding','Refused','No Longer Required','Agreed Not Expired', 'Agreed Expired')""")
Select_CP2_Status_Areas = arcpy.Select_analysis(Select_AccessLicence_data,str(Working)+"\Select_CP2_Areas","""In_CP2_Limits_Int = 1 AND Status = 'Not Issued' AND SHAPE_Area > 4046.68 OR In_CP2_Limits_Int = 1 AND Status IN( 'Outstanding','Refused','No Longer Required','Agreed Not Expired', 'Agreed Expired')""")
Select_L3L4_Status_Areas = arcpy.Select_analysis(Select_AccessLicence_data,str(Working)+"\Select_L3L4_Areas","""In_L3L4_Limits_Int = 1 AND Status = 'Not Issued' AND SHAPE_Area > 4046.68 OR In_L3L4_Limits_Int = 1 AND Status IN( 'Outstanding','Refused','No Longer Required','Agreed Not Expired', 'Agreed Expired')""")
Select_MML_Status_Areas = arcpy.Select_analysis(Select_AccessLicence_data,str(Working)+"\Select_MML_Areas","""In_MML_Limits_Int = 1 AND Status = 'Not Issued' AND SHAPE_Area > 4046.68 OR In_MML_Limits_Int = 1 AND Status IN( 'Outstanding','Refused','No Longer Required','Agreed Not Expired', 'Agreed Expired')""")
Select_CP2_1_Status_Areas = arcpy.Select_analysis(Select_AccessLicence_data,str(Working)+"\Select_CP2_1_Areas","""In_CP2_1_Limits_Int = 1 AND Status = 'Not Issued' AND SHAPE_Area > 4046.68 OR In_CP2_1_Limits_Int = 1 AND Status IN( 'Outstanding','Refused','No Longer Required','Agreed Not Expired', 'Agreed Expired')""")
Select_CP3_Status_Areas = arcpy.Select_analysis(Select_AccessLicence_data,str(Working)+"\Select_CP3_Areas","""In_CP3_Limits_Int = 1 AND Status = 'Not Issued' AND SHAPE_Area > 4046.68 OR In_CP3_Limits_Int = 1 AND Status IN( 'Outstanding','Refused','No Longer Required','Agreed Not Expired', 'Agreed Expired')""")

print 'Selection of limits layers complete'
##print 'selects complete'
##print 'Test stuff'
Dissolve_select_CP2_1_250_on_Status = arcpy.Dissolve_management(Select_CP2_1_250_Status_Areas,str(Working)+'\Dissolve_CP2_1_250_Status',"Status")
Dissolve_select_CP2_on_Status = arcpy.Dissolve_management(Select_CP2_Status_Areas,str(Working)+'\Dissolve_CP2_Status',"Status")
Dissolve_select_L3L4_on_Status = arcpy.Dissolve_management(Select_L3L4_Status_Areas,str(Working)+'\Dissolve_L3L4_Status',"Status")
Dissolve_select_MML_on_Status = arcpy.Dissolve_management(Select_MML_Status_Areas,str(Working)+'\Dissolve_MML_Status',"Status")
Dissolve_select_CP2_1_on_Status = arcpy.Dissolve_management(Select_CP2_1_Status_Areas,str(Working)+'\Dissolve_CP2_1_Status',"Status")
Dissolve_select_CP3_on_Status = arcpy.Dissolve_management(Select_CP3_Status_Areas,str(Working)+'\Dissolve_CP3_Status',"Status")

print 'Dissolve on status complete'


Summary_Stats_CP2_1_250 = arcpy.Statistics_analysis(Select_CP2_1_250_Status_Areas,str(Working)+'\CP2_1_250_Summary_stats',[["Status","COUNT"]], "Status")
Summary_Stats_CP2 = arcpy.Statistics_analysis(Select_CP2_Status_Areas,str(Working)+'\CP2_Summary_stats',[["Status","COUNT"]], "Status")
Summary_Stats_L3L4 = arcpy.Statistics_analysis(Select_L3L4_Status_Areas,str(Working)+'\L3L4_Summary_stats',[["Status","COUNT"]], "Status")
Summary_Stats_MML = arcpy.Statistics_analysis(Select_MML_Status_Areas,str(Working)+'\MML_Summary_stats',[["Status","COUNT"]], "Status")
Summary_Stats_CP2_1 = arcpy.Statistics_analysis(Select_CP2_1_Status_Areas,str(Working)+'\CP2_1_Summary_stats',[["Status","COUNT"]], "Status")
Summary_Stats_CP3 = arcpy.Statistics_analysis(Select_CP3_Status_Areas,str(Working)+'\CP3_Summary_stats',[["Status","COUNT"]], "Status")

print 'Summary Stats complete per limits'

Convert_to_Excel_Summary_Stats_CP2_1_250 = arcpy.TableToExcel_conversion(Summary_Stats_CP2_1_250, str(createprojectfolder)+'\SummaryStats_CP2_1_250.xls')
Convert_to_Excel_Summary_Stats_CP2 = arcpy.TableToExcel_conversion(Summary_Stats_CP2, str(createprojectfolder)+'\SummaryStats_CP2_.xls')
Convert_to_Excel_Summary_Stats_L3L4 = arcpy.TableToExcel_conversion(Summary_Stats_L3L4, str(createprojectfolder)+'\SummaryStats_L3L4_.xls')
Convert_to_Excel_Summary_Stats_MML = arcpy.TableToExcel_conversion(Summary_Stats_MML, str(createprojectfolder)+'\SummaryStats_MML_.xls')
Convert_to_Excel_Summary_Stats_CP2_1 = arcpy.TableToExcel_conversion(Summary_Stats_CP2_1, str(createprojectfolder)+'\SummaryStats_CP2_1.xls')
Convert_to_Excel_Summary_Stats_CP3 = arcpy.TableToExcel_conversion(Summary_Stats_CP3, str(createprojectfolder)+'\SummaryStats_CP3.xls')

print 'Summary stats converted to excel'

Convert_to_Excel_Dissolve_CP2_1_250 = arcpy.TableToExcel_conversion(Dissolve_select_CP2_1_250_on_Status, str(createprojectfolder)+'\Status_Area_CP2_1_250.xls')
Convert_to_Excel_Dissolve_CP2 = arcpy.TableToExcel_conversion(Dissolve_select_CP2_on_Status, str(createprojectfolder)+'\Status_Area_CP2_.xls')
Convert_to_Excel_Dissolve_L3L4 = arcpy.TableToExcel_conversion(Dissolve_select_L3L4_on_Status, str(createprojectfolder)+'\Status_Area_L3L4_.xls')
Convert_to_Excel_Dissolve_MML = arcpy.TableToExcel_conversion(Dissolve_select_MML_on_Status, str(createprojectfolder)+'\Status_MML_Area_.xls')
Convert_to_Excel_Dissolve_CP2_1 = arcpy.TableToExcel_conversion(Dissolve_select_CP2_1_on_Status, str(createprojectfolder)+'\Status_Area_CP2_1.xls')
Convert_to_Excel_Dissolve_CP3 = arcpy.TableToExcel_conversion(Dissolve_select_CP3_on_Status, str(createprojectfolder)+'\Status_Area_CP3.xls')

print 'Dissolve to excel complete'

endtime = datetime.now() - start

Select_Sub_Project_Stats_L3L4 = arcpy.Select_analysis(Select_AccessLicence_data,str(Working)+'\Sub_Project_L3L4',"""Sub_Project = 'L3L4'""")
Select_Sub_Project_Stats_MML = arcpy.Select_analysis(Select_AccessLicence_data,str(Working)+'\Sub_Project_MML',"""Sub_Project = 'MML'""")

print 'Selected Sub Project fields complete'

Dissolve_SubP_L3L4 = arcpy.Dissolve_management(Select_Sub_Project_Stats_L3L4,str(Working)+'\Diss_Subproject_L3L4',"Status")
Dissolve_SubP_MML = arcpy.Dissolve_management(Select_Sub_Project_Stats_MML(Working)+'\Diss_Subproject_MML',"Status")

print 'Sub P Dissolve complete'

Summary_Stats_SubP_L3L4 = arcpy.Statistics_analysis(Select_Sub_Project_Stats_L3L4,str(Working)+'\Summary_Stats_SubP_L3L4',[["Status","COUNT"]],"Status")
Summary_Stats_SubP_MML = arcpy.Statistics_analysis(Select_Sub_Project_Stats_MML,str(Working)+'\Summary_Stats_SubP_MML',[["Status","COUNT"]],"Status")

print 'Sub P summary Stats Complete'

SubP_Table_to_Excel_L3L4_Area = arcpy.TableToExcel_conversion(Dissolve_SubP_L3L4,str(createprojectfolder)+'\SubP_L3L4_Status_Area')
SubP_Table_to_Excel_MML_Area = arcpy.TableToExcel_conversion(Dissolve_SubP_MML,str(createprojectfolder)+'\SubP_MML_Status_Area')
SubP_Table_to_Excel_L3L4_Summary = arcpy.TableToExcel_conversion(Summary_Stats_SubP_L3L4,str(createprojectfolder)+'\SubP_L3L4_Summary')
SubP_Table_to_Excel_MML_Summary = arcpy.TableToExcel_conversion(Summary_Stats_SubP_MML,str(createprojectfolder)+'\SubP_L3L4_Summary')

print 'Sub Project table to excel complete'

print 'script complete'