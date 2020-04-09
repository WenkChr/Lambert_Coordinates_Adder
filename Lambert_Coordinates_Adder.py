import arcpy, os

arcpy.env.overwriteOutput = True

# Function
def coordinates_to_lambert(fc, prj, out_fc_name, outGDB):
    # Check if fc in Lambert coordinate system if not reproject
    transform = arcpy.ListTransformations(arcpy.Describe(fc).spatialReference, prj)
    if len(transform) != 0:
        arcpy.env.geographicTransformation = transform[0]
    
    transform = [0]
    fc_projected = arcpy.Project_management(fc, os.path.join(outGDB, out_fc_name), prj)
    arcpy.AddFields_management(fc_projected, [['Lambert_X', 'DOUBLE'], ['Lambert_Y', 'DOUBLE']])
    arcpy.AddXY_management(fc_projected)
    arcpy.CalculateFields_management(fc_projected, 'PYTHON3', [['Lambert_X', '!POINT_X!'], ['Lambert_Y', '!POINT_Y!']])
    arcpy.DeleteField_management(fc_projected, ['POINT_X', 'POINT_Y', 'POINT_Z', 'POINT_M'])    

# Constants
workingGDB = r'H:\Lambert_Coordinates_Adder\LambertCoords.gdb'
Test_fc = os.path.join(workingGDB, 'city_of_yellow_knife') # Test File to get lambert coordinates, mu
prj_file = r'H:\Lambert_Coordinates_Scripts\PCS_Projection.prj' # Path to .prj file or arcpy.SpatialReference object

# Calls
coordinates_to_lambert(Test_fc, prj_file, 'yellow_knife_lambert', workingGDB)

print('DONE!')