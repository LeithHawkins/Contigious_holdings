import arcpy


fields = arcpy.ListFields("B:\\Non_Contigous_Working\\Non_Contiguos_Working.gdb\\test_Output\\holding_108009671")

for field in fields:
    print("{0} "
          .format(field.name))


'Holding_Name'
'Holding_Location_Address'
"Local_Land_Services_Region_Id
Local_Land_Services_Region_Name
RLPB_Board_Name
Property_Identification_Code
Occupier_Id
Occupier_Full_Name
Occupier_Mailing_Address
Occupier_Home_Phone
Occupier_Mobile_Phone
Occupier_Email_Address
Total_Area
Is_Rateable_Indicator
Rateable_Area
Nominal_Notional_Carrying_Cap
SHAPE_STArea__
SHAPE_STLength__
ORIG_FID
'NEAR_FID
'NEAR_DIST
'Shape_Length
'Shape_Area'


