import arcpy
from arcpy import env
import time

start = time.time()
arcpy.env.overwriteOutput = True
# Set File workspace
file_workspace = 'B:\\Risk\\Risk.gdb'
env.workspace = file_workspace
