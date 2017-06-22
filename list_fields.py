import arcpy


fields = arcpy.ListFields("B:\\Non_Contigous_Working\\Non_Contiguos_Working.gdb\\test_Output\\holding_108009671")

for field in fields:
    print("{0} "
          .format(field.name))




