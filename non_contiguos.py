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
        holding = 'Holding' + refNumber
        start = time.time()
        arcpy.SelectLayerByAttribute_management('Holdings_Layer', 'NEW_SELECTION',
                                                "Holding_Reference_Number = " + str(row[0]))

        arcpy.Buffer_analysis('Holdings_Layer', 'in_memory/holding_bufferfirst',
                              "200 Meters", "FULL", "ROUND", "LIST", "Holding_Reference_Number", "PLANAR")
        arcpy.Buffer_analysis('in_memory/holding_bufferfirst', 'in_memory/holding_buffersecond',
                              "-200 Meters", "FULL", "ROUND", "LIST", "Holding_Reference_Number", "PLANAR")

        arcpy.MultipartToSinglepart_management(
            'in_memory/holding_buffersecond', 'in_memory/holding_Buffer')
        dataset = 'in_memory/holding_Buffer'
        dataset_dissolve = 'in_memory/holding_dissolve'
        out_Table = 'in_memory/output_table'

        result = arcpy.GetCount_management(dataset)
        count = int(result.getOutput(0))
        if count > 1:
            test_Output = 'B:\\Non_Contigous_Working\\Non_Contiguos_Working.gdb'
            large_Output = 'B:\\Non_Contigous_Working\\Non_Contiguos_Working.gdb\\test_Output'

            arcpy.GenerateNearTable_analysis(
                dataset, dataset, out_Table, '', 'NO_LOCATION', 'NO_ANGLE', 'All')

            def unique_values(table, Field):
                with arcpy.da.SearchCursor(table, [Field]) as cursor:
                    return sorted({row[0] for row in cursor})

            Mval = max(unique_values(out_Table, 'NEAR_DIST'))

            if Mval > 200:
                field_name = 'Max_Distance'
                arcpy.Dissolve_management(dataset, dataset_dissolve, [
                                          'Holding_Reference_Number'])
                arcpy.AddField_management(
                    dataset_dissolve, field_name, 'FLOAT', '', '', '', '')

                with arcpy.da.UpdateCursor(dataset_dissolve, ['Max_Distance']) as large:
                    for row in large:
                        row[0] = Mval
                        large.updateRow(row)
                        print row[0]
                        print large.updateRow(row)
                        fields = arcpy.ListFields('in_memory/holding_dissolve')

                output_Fc = 'B:\\Non_Contigous_Working\\Non_Contiguos_Working.gdb\\output\\Holdings_Multiple'
                arcpy.Append_management(
                    dataset_dissolve, output_Fc, 'TEST', '', '')
                print'Near Complete'
                arcpy.Delete_management('in_memory/holding_bufferfirst')
                arcpy.Delete_management('in_memory/holding_buffersecond')
                arcpy.Delete_management(dataset)
                arcpy.Delete_management(dataset_dissolve)
                arcpy.Delete_management(out_Table)
                del row
                #finish



    print('Time: ' + str(time.time() - start))
