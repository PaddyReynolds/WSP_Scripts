#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKKXR602
#
# Created:     08/11/2019
# Copyright:   (c) UKKXR602 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Description
# -----------
# This script is intended to be used by the WSP GIS team, when performing SDE Administration tasks. It follows the recommended ESRI workflow for SDE administration: Reconcile and Post
# versions > Compress database > Rebuild Indexes > Analyze datasets. The compression is run three times in order to get as close to 0 states and lineages as possible.
# Logging is built into the script and the logfile will be located in the path specified in the 'root' variable.
# Written for ArcGIS version: 10.0 and above
# Adapted from a script written bu Chris Snyder, WA Department of Natural Resources, chris.snyder(at)wadnr.gov by Ollie Brown, Senior GIS Consultant, WSP
# Date last updated: 16/11/2017

try:
    #Import system modules
    import sys, os, time, traceback, arcpy, subprocess

    #Define functions to get messages from the geoprocessor and python
    def showGpMessage():
        arcpy.AddMessage(arcpy.GetMessages())
        print >> open(logFile, 'a'), arcpy.GetMessages()
        print arcpy.GetMessages()
    def showPyMessage():
        arcpy.AddMessage(str(time.ctime()) + " - " + message)
        print >> open(logFile, 'a'), str(time.ctime()) + " - " + message
        print str(time.ctime()) + " - " + message

    Workspace_name = arcpy.GetParameterAsText(0)
    #Email_Address = arcpy.GetParameterAsText(0)

    #Specify root directory variable, define logFile variable and minor error checking
    root = r"C:\SCHEME_DOWNLOAD\Log" #Log file location
    if os.path.exists(root)== False:
        print "ERROR: SPECIFIED LOG FILE LOCATION " + root + " DOES NOT EXIST... EXITING SCRIPT";time.sleep(3);sys.exit()
    dateTimeStamp = time.strftime('%Y%m%d%H%M%S') #in the format YYYYMMDDHHMMSS
    logFile = root + "\\" + "SDE_Admin_Logfile" + "_" + dateTimeStamp + ".txt" #Creates the logFile variable

    #Sets some gp envr settings...
    arcpy.env.overwriteOutput = True
    arcpy.env.logHistory = True

    message = "Starting SDE Administration Tasks..."; showPyMessage()
    #*****************GEOPROCESSING SECTION STARTS******************************

    # ENVIRONMENT
    # set workspace
    arcpy.env.workspace = Workspace_name
    #'Database Connections/WSP NG_Glaslyn_Cables DEFAULT SDE.sde'

    # set the workspace environment
    workspace = arcpy.env.workspace

    # COMPRESSION
    # Block new connections to the database
    #NEED TO CHECK THIS AND ADD BACK IN. WASN'T ALLOWING CONNECTIONS AFTERWARDS arcpy.AcceptConnections(workspace, False); showGpMessage()
    #NEED TO CHECK THIS AND ADD BACK IN. WASN'T ALLOWING CONNECTIONS AFTERWARDS message = "DB connections denied"; showPyMessage()

    # Disconnect all users from the database
    #WORKS IF COMMENT OUT THIS BIT
    #NEED TO CHECK THIS AND ADD BACK IN. WASN'T ALLOWING CONNECTIONS AFTERWARDS arcpy.DisconnectUser(workspace, "ALL"); showGpMessage()
    #NEED TO CHECK THIS AND ADD BACK IN. WASN'T ALLOWING CONNECTIONS AFTERWARDS message = "Users disconnected"; showPyMessage()

    # Get a list of versions to pass into the ReconcileVersions tool
    #versionList = arcpy.ListVersions(workspace)
    #message = "Versions Listed"; showPyMessage()

    # Execute the ReconcileVersions tool
    #arcpy.ReconcileVersions_management(workspace, "ALL_VERSIONS", "SDE.DEFAULT", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION", ""); showGpMessage()
    #message = "Reconciling versions completed"; showPyMessage()

    # Run the compress tool 1st pass
    arcpy.Compress_management(workspace); showGpMessage()
    message = "First compression completed"; showPyMessage()

    # Wait 5 seconds
    time.sleep(5)

    # Run the compress tool 2nd pass
    arcpy.Compress_management(workspace); showGpMessage()
    message = "Second compression completed"; showPyMessage()

    # Wait 5 seconds
    time.sleep(5)

    # Run the compress tool 3rd pass
    arcpy.Compress_management(workspace); showGpMessage()
    message = "Third compression completed"; showPyMessage()

    # Allow the database to begin accepting connections again
    #NEED TO CHECK THIS AND ADD BACK IN. WASN'T ALLOWING CONNECTIONS AFTERWARDS arcpy.AcceptConnections(workspace, True); showGpMessage()
    #NEED TO CHECK THIS AND ADD BACK IN. WASN'T ALLOWING CONNECTIONS AFTERWARDS message = "DB connections accepted"; showPyMessage()

    # REBUILD INDEXES
    # List Accessible datasets
    # Accessible stand alone tables, feature classes and rasters:
    dataList = arcpy.ListTables() + arcpy.ListFeatureClasses() + arcpy.ListRasters()
    arcpy.AddMessage(str(dataList))
    # Add accessible datasets and featureclasses within datasets to master list
    for dataset in arcpy.ListDatasets("", "Feature"):
        arcpy.env.workspace = os.path.join(workspace,dataset)
        dataList += arcpy.ListFeatureClasses() + arcpy.ListDatasets()

    # Reset workspace
    arcpy.env.workspace = workspace

    # Get workspace username
    userName = arcpy.Describe(workspace).connectionProperties.user.lower()

    # Remove datasets not owned by connected user from master list
    userDataList = [ds for ds in dataList if ds.lower().find(".%s." % userName) > -1]

    # Execute Rebuild Indexes
    # Note: to use the "SYSTEM" option the workspace user must be an administrator.
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", userDataList, "ALL"); showGpMessage()
    message = "Rebuilding indexes complete"; showPyMessage()

    # ANALYZE DATA
    # List Accessible datasets
    # Accessible stand alone tables, feature classes and rasters:
    dataList = arcpy.ListTables() + arcpy.ListFeatureClasses() + arcpy.ListRasters()

    # Add accessible datasets and featureclasses within datasets to master list
    for dataset in arcpy.ListDatasets("", "Feature"):
        arcpy.env.workspace = os.path.join(workspace,dataset)
        dataList += arcpy.ListFeatureClasses() + arcpy.ListDatasets()

    # Reset workspace
    arcpy.env.workspace = workspace

    # Get workspace username
    userName = arcpy.Describe(workspace).connectionProperties.user.lower()

    # Remove datasets not owned by connected user from master list
    userDataList = [ds for ds in dataList if ds.lower().find(".%s." % userName) > -1]

    # Execute Analyze
    # Note: to use the "SYSTEM" option the workspace user must be an administrator.
    arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE","ANALYZE_DELTA","ANALYZE_ARCHIVE"); showGpMessage()
    message = "Analyzing data complete"; showPyMessage()

    #subprocess.call ("C:\SCHEME_DOWNLOAD\SendEmail.py", "Peadar.Kelly@wsp.com", "Admin tasks completed for")

    #*****************GEOPROCESSING SECTION ENDS******************************
    message = "Ending SDE Administration Tasks..."; showPyMessage()

    #Indicates that the script is complete
    message = sys.argv[0] + " is complete!"; showPyMessage()
except:
    message = "\n*** LAST GEOPROCESSOR MESSAGE (may not be source of the error)***"; showPyMessage()
    showGpMessage()
    message = "\n*** PYTHON ERRORS *** "; showPyMessage()
    message = "Python Traceback Info: " + traceback.format_tb(sys.exc_info()[2])[0]; showPyMessage()
    message = "Python Error Info: " +  str(sys.exc_type) + ": " + str(sys.exc_value) + "\n"; showPyMessage()
    message = "\n*** PYTHON LOCAL VARIABLE LIST ***"; showPyMessage()
    variableCounter = 0
    while variableCounter < len(locals()):
        message =  str(list(locals())[variableCounter]) + " = " + str(locals()[list(locals())[variableCounter]]); showPyMessage()
        variableCounter = variableCounter + 1

   # subprocess.call ("C:\SCHEME_DOWNLOAD\SendEmail.py" EmailAddress "Admin tasks failed for " + Workspace_name, shell=False)

