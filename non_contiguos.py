import arcpy
from arcpy import env
import time

#Settings
baseDirectory = 'B:\\Non_Contigous_Working'
fileworkspace = baseDirectory + '\\Non_Contiguos_Working.gdb'
Holdings = fileworkspace + '\\Holding\\NTLLS_Holding_190617'

#arcpy Settings
arcpy.env.overwriteOutput = True
env.workspace = fileworkspace


arcpy.MakeFeatureLayer_management(Holdings, 'Holdings_Layer')

with arcpy.da.SearchCursor(Holdings, ['Holding_Reference_Number'])as Holdings_Ref_cursor:
    for row in Holdings_Ref_cursor:
        start = time.time()
        refNumber = str(row[0])
print 'Holding:' + refNumber
arcpy.Select_analysis('Holdings_Layer', 'in_memory/holding', "Holding_Reference_Number = " + refNumber)

arcpy.MultipartToSinglepart_management('Holdings_Layer', 'in_memory/holding_single')

#print('Time: ' + str(time.time() - start))
