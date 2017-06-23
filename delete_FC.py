import arcpy
import fnmatch
from arcpy import env
import time

baseDirectory = 'B:\\Non_Contigous_Working'
fileworkspace = baseDirectory + '\\Non_Contiguos_Working.gdb'
Holdings = fileworkspace + '\\test_Output\\Holding_test'
# arcpy Settings
arcpy.env.overwriteOutput = True
env.workspace = fileworkspace


# variables:
fcs = arcpy.ListFeatureClasses()
filtered = fnmatch.filter(fcs, 'holding*')
print filtered

# Delete selected fcs
for fc in filtered:
    if arcpy.Exists(fc):
        arcpy.Delete_management(fc)
