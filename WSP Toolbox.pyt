import arcpy
import math


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "WSPToolbox"
        self.alias = "WSP Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [ExtentCalculator]


class ExtentCalculator(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Extent Calculator"
        self.description = "This tool updates scale of the map based on the extent of the LAA feature shown in current DDP page."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
	# First parameter
    	param0 = arcpy.Parameter(
        displayName="Input Features",
        name="in_features",
        datatype="GPFeatureLayer",
        parameterType="Required",
        direction="Input")
		
	# Second parameter
    	param1 = arcpy.Parameter(
        displayName='Select page size',
        name='page_size',
        datatype='GPString',
        parameterType='Required',
        direction='Input',
	multiValue=False)
	param1.value = 'A3'
	param1.filter.list = ['LETTER', 'LEGAL', 'TABLOID', 'A5', 'A4', 'A3', 'A2', 'A1', 'A0', 'C', 'D', 'E']


        params = [param0, param1]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
		
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""				
        lyr = parameters[0].valueAsText
	pageSize = parameters[1].value
	arcpy.AddMessage("layer = {}, Page size = {}".format(lyr, pageSize))
			 
	def iScale(xMin, yMin, xMax, yMax, pSize):
		scaleRange = [1250, 2500, 5000, 7500, 10000]
		diagonal = float(math.sqrt((xMax-xMin)*(xMax-xMin) + (yMax-yMin)*(yMax-yMin)))
		initialScale = 10000
		for scale in scaleRange:
			xTent = ((scale/100)*int(pSize))
			if (diagonal < xTent):
				initialScale = scale
				break	
		return initialScale
		 
	pageSize_min = {'LETTER': '20', 'LEGAL': '20', 'TABLOID': '26', 'A5': '13', 'A4': '19', 'A3': '28', 'A2': '40', 'A1': '57', 'A0': '82', 'C': '41', 'D': '54', 'E': '84'}	
	arcpy.AddMessage("Sunil..")		
	with arcpy.da.UpdateCursor("{}".format(lyr), ["SHAPE@", "Notice_Plan_Input_Notice_Number", "Scale"]) as updateRows:
		arcpy.AddMessage("Karde..")
		for updateRow in updateRows:
			extent = updateRow[0].extent
			arcpy.AddMessage("extent.XMin = ".format(extent.XMin))
			array = arcpy.Array([arcpy.Point(extent.XMin, extent.YMin), arcpy.Point(extent.XMax, extent.YMin), arcpy.Point(extent.XMax, extent.YMax), arcpy.Point(extent.XMin, extent.YMax)])
			polygon = arcpy.Polygon(array)
			Intial_Scale = iScale((extent.XMin), (extent.YMin), (extent.XMax), (extent.YMax), pageSize_min["{}".format(pageSize)])
			updateRow[2] = float(Intial_Scale)
			arcpy.AddMessage("pageSize_min = {}, Intial_Scale = {}".format(pageSize_min["{}".format(pageSize)], Intial_Scale))
			updateRows.updateRow(updateRow)
		del updateRows	
	
    	return
