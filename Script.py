'''**********************************************************

	Jefferson Valencia Gomez - Unsupervised Classification
	
**********************************************************'''

print ""
print ""
print "***************************************************************"
print "      		Initializing Libraries"
print "***************************************************************"
print ""
print ""

from pci.kclus import *
from pci.sieve import *
from pci.fexport import *
from pci.exceptions import *
import arcpy
from arcpy import env
import arcpy.mapping
import locale
import os
import calendar, time

arcpy.CheckOutExtension("Spatial") #Licensing the ArcGIS Spatial Analyst extension
arcpy.env.overwriteOutput = True
print "ESRIs ArcPy environment successfully loaded"

#This section of code is added to ensure that Python is properly configured in that same was as PCIs C/C++ code
locale.setlocale( locale.LC_ALL, "" )
locale.setlocale( locale.LC_NUMERIC, "C" )

print ""
print "Initialization Complete"
print ""

start_time = calendar.timegm(time.gmtime()) #Current time in seconds since epoch

inputs = r"D:\Dropbox\Masters\Msc_in_Geospatial_Technologies\Courses\Remote_Sensing_SIW007\Project\Python_Project\inputs"
outputs = r"D:\Dropbox\Masters\Msc_in_Geospatial_Technologies\Courses\Remote_Sensing_SIW007\Project\Python_Project\outputs"

if not os.path.exists(outputs): 
    os.makedirs(outputs)

print ""
print "***************************************************************"
print "              Geomatica - Running K-Means Clustering"
print "***************************************************************"
print ""


file = inputs + "\\golden_horseshoe.pix"
dbic = [1,2,3,4,5,6]	# input channels
dboc = [7]	# output channel
mask = []	# process entire image
numclus = [30]	# requested number of clusters
seedfile = u""	#  automatically generate seeds
maxiter = [30]	# no more than 30 iterations
movethrs = [0.01]
siggen = u""	# do not generate signatures
backval = []	# no background value
nsam = []	# default number of sample points

if os.path.isfile(file):
    print "found the file: " + file
else:
    print "Could not find " + file + "\n\nPlease check that the file exists\
    AND that the path is correct."
    exit()

try:
	kclus(file, dbic, dboc, mask, numclus, seedfile, maxiter, movethrs, siggen, backval, nsam)
except PCIException, e:
    print e
except Exception, e:
    print e

print "K-Means Clusters Complete!"
print ""

print ""
print "***************************************************************"
print "              Geomatica - Running SIEVE Filter"
print "***************************************************************"
print ""

dbic2 = [7] #Input raster channel
dboc2 = [8] #Output raster channel
sthresh = [128]	# polygon size threshold
keepvalu = []	# no keep value
connect	= []	# default, 4-connection

try:
	sieve( file, dbic2, dboc2, sthresh, keepvalu, connect )
except PCIException, e:
    print e
except Exception, e:
    print e

print "SIEVE Filtering Complete!"
print ""

print ""
print "***************************************************************"
print "              Geomatica - Export SIEVE Filter to 32bit GeoTIFF"
print "***************************************************************"
print ""

filo	=	outputs + '\\sieve_filter.tif'
dbiw	=	[]
dbic3	=	[8] #Output raster channel
dbib	=	[]
dbvs	=	[]
dblut	=	[]
dbpct	=	[]
ftype	=	"TIF"
foptions =  u""

try:
	fexport( file, filo, dbiw, dbic3, dbib, dbvs, dblut, dbpct, ftype, foptions )
except PCIException, e:
    print e
except Exception, e:
    print e

print "Export Complete!"
print ""

print ""
print "***************************************************************"
print "              ArcGIS - Convert Raster To Polygon"
print "***************************************************************"
print ""

print "Creating File Geodatabase"
# Execute RasterToPolygon
try:
    arcpy.CreateFileGDB_management(outputs, 'final_classification.gdb') #Create output file GeoDatabase
except Exception, e:
    print e
print "File Geodatabase created successfully!"
print ""

geodatabase_file = outputs + '\\final_classification.gdb'

# Set local variables
inRaster = filo
outPolygons = geodatabase_file + '\\sieve_filter_class'
field = "VALUE"

# Execute RasterToPolygon
try:
	arcpy.RasterToPolygon_conversion(inRaster, outPolygons, "NO_SIMPLIFY", field)
except Exception, e:
    print e
print "Conversion Complete!"
print ""

print "Dissolving features"
dissPolygons = geodatabase_file + '\\final_classification'
try:
    arcpy.Dissolve_management(outPolygons, dissPolygons, "gridcode", "", "MULTI_PART", "DISSOLVE_LINES")
except Exception, e:
    print e
print "Dissolve applied successfully!"
print ""

print ""
print "***************************************************************"
print "                ArcGIS - Creating ArcMap Project                 "
print "***************************************************************"
print ""

map_doc = inputs + "\\template.mxd" 

print "Gathering Output files"
print""

# get the map document 
mxd = arcpy.mapping.MapDocument(map_doc)  

# get the data frame 
df = arcpy.mapping.ListDataFrames(mxd,"*")[0]

# create a new layer
class_raster = arcpy.mapping.Layer(filo)
filter_layer = arcpy.mapping.Layer(outPolygons)
class_layer = arcpy.mapping.Layer(dissPolygons)

layer_list = [class_raster, filter_layer, class_layer]
 
# add the layer to the map at the bottom of the TOC in data frame 0 
for add_layers in layer_list:
    arcpy.mapping.AddLayer(df, add_layers,"TOP")
    
#arcpy.MakeRasterLayer_management(mosaic_file, "Mosaic_tif3", "", "248886 5184779.25 251513.25 5187957", "")
    
map_file_final = outputs + '\\Class_analysis.mxd'

# make a copy of the mxd file
mxd.saveACopy(map_file_final)

# open the final mxd file
os.system("start " + map_file_final)

print ""
print "ALL PROCESSING COMPLETE!"
print ""

end_time = calendar.timegm(time.gmtime()) #Current time in seconds since epoch

process_time = end_time - start_time

print "Processing took " + str(process_time) + " seconds!"