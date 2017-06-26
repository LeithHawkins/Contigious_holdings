

import arcpy


fields = arcpy.ListFields('B:\\Non_Contigous_Working\\Non_Contiguos_Working.gdb\\holding108009671')

for field in fields:
    print("{0} is a type of {1} with a length of {2}"
          .format(field.name, field.type, field.length))
