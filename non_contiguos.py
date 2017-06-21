import arcpy
from arcpy import env
import time
# Settings
baseDirectory = 'B:\\Non_Contigous_Working'
fileworkspace = baseDirectory + '\\Non_Contiguos_Working.gdb'
Holdings = fileworkspace + '\\Holding\\NTLLS_Holding_190617'
# arcpy Settings
arcpy.env.overwriteOutput = True
env.workspace = fileworkspace
# SearchCursor
arcpy.MakeFeatureLayer_management(Holdings, 'Holdings_Layer')

with arcpy.da.SearchCursor(Holdings, ['Holding_Reference_Number']) as Holdings_Ref_cursor:
    for row in Holdings_Ref_cursor:
        refNumber = str(row[0])
        print 'Holding:' + refNumber
        start = time.time()
        arcpy.SelectLayerByAttribute_management('Holdings_Layer', 'NEW_SELECTION',
                                                "Holding_Reference_Number = " + str(row[0]))
        arcpy.MultipartToSinglepart_management(
            'Holdings_Layer', 'in_memory/holding_single')
        dataset = 'in_memory/holding_single'
        output_Fc = 'B:\\Non_Contigous_Working\\Non_Contiguos_Working.gdb\\Holding\\Holding_Near_Complete'
        result = arcpy.GetCount_management(dataset)
        count = int(result.getOutput(0))
        if count > 1:
            arcpy.Near_analysis(dataset, dataset)
            arcpy.Append_management('in_memory/holding_single', output_Fc )
            print 'Near Complete'
        print('Time: ' + str(time.time() - start))
