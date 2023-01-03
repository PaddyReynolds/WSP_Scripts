-----------------------------------------------
arcpy.env.overwriteOutput = True

#Create local GDB & work folders
arcpy.AddMessage("Creating Local Copy")
desktopPath = os.environ.get( "USERPROFILE" ) + "\\Desktop"
if os.path.isdir(desktopPath) == False:
    os.makedirs(desktopPath + "\\PlotNumberingScratch")
TempFolder = desktopPath + "\\PlotNumberingScratch"
ScratchGDD = "PlotScratch"
WorkGDD = TempFolder + "\\" + ScratchGDD + ".gdb"
dissolvedPlots = WorkGDD + "\\" + "DissolvedPlots"
if os.path.isdir(desktopPath) == False:
    arcpy.CreateFileGDB_management(TempFolder,ScratchGDD)