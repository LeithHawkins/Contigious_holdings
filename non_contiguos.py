import arcpy
from arcpy import env
import time
# Settings
baseDirectory = 'B:\\Non_Contigous_Working'
fileworkspace = baseDirectory + '\\Non_Contiguos_Working.gdb'
Holdings = fileworkspace + '\\test_Output\\Holding_test'
# arcpy Settings
arcpy.env.overwriteOutput = True
env.workspace = fileworkspace

# SearchCursor
arcpy.MakeFeatureLayer_management(Holdings, 'Holdings_Layer')

with arcpy.da.SearchCursor(Holdings, ['Holding_Reference_Number']) as Holdings_Ref_cursor:
    for row in Holdings_Ref_cursor:
        refNumber = str(row[0])
        print 'Holding:' + refNumber
        holding = 'Holding' + refNumber
        start = time.time()
        arcpy.SelectLayerByAttribute_management('Holdings_Layer', 'NEW_SELECTION',
                                                "Holding_Reference_Number = " + str(row[0]))
        arcpy.MultipartToSinglepart_management(
            'Holdings_Layer', 'in_memory/holding_single')
        dataset = 'in_memory/holding_single'
        dataset_dissolve = 'in_memory/holding_dissolve'
        out_Table = 'in_memory/output_table'
        print out_Table

        result = arcpy.GetCount_management(dataset)
        count = int(result.getOutput(0))
        if count > 1:
            test_Output = 'B:\\Non_Contigous_Working\\Non_Contiguos_Working.gdb'
            large_Output = 'B:\\Non_Contigous_Working\\Non_Contiguos_Working.gdb\\test_Output\\'

            arcpy.GenerateNearTable_analysis(
                dataset, dataset, out_Table, '', 'NO_LOCATION', 'NO_ANGLE', 'All')

            def unique_values(table, Field):
                with arcpy.da.SearchCursor(table, [Field]) as cursor:
                    return sorted({row[0] for row in cursor})
            #unique_values(out_Table ,'NEAR_DIST')
            large = max(unique_values(out_Table, 'NEAR_DIST'))
            if large > 200:
                field = 'Max_Distance'
                arcpy.Dissolve_management(dataset,dataset_dissolve, ['Holding_Reference_Number'])
                arcpy.AddField_management(dataset_dissolve, field, 'DOUBLE', '', '','','')
                while row:
                    row.setValue(field, row.getValue(large))
                    cursor.updateRow(row)
                    row = cursor.next()
                    pass
                #     arcpy.FeatureClassToFeatureClass_conversion(dataset, large_Output, 'holding_'+ refNumber )

                #output_Fc = 'B:\\Non_Contigous_Working\\Non_Contiguos_Working.gdb\\Holding\\Holding_Near_Complete'
                #arcpy.Append_management('in_memory/holding_single', output_Fc, 'NO_TEST','','')
                print'Near Complete'
    print('Time: ' + str(time.time() - start))
