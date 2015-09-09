# Remote Sensing Project - ArcGIS and Geomatica Customization

## Final project of remote sensing subject

Both ArcGIS and Geomatica offer a complete range of possibilities to make easier and automate workflows in order to give customized geospatial solutions.
The Python script "Script.py" executes and automates workflow in both programs.

Before to start it is important to have both software installed. It is necessary the Spatial Analyst extension of ArcGIS. Then install the “ArcGIS for Desktop Background Geoprocessing (64 bit)” and use it to incorporate PCI’s Python library in the script. Remember to enter the PCI’s library into the environmental variables of Windows.

The Python script runs an unsupervised classification (by applying K-Means Clustering) followed by a SIEVE filtering, vectorization and exportation to shape file of the final result.

The stepst executed by the script are the following:

1. K-Means Clustering
2. SIEVE Filter
3. Export SIEVE Filter result to 32bit GeoTIFF
4. Convert Raster to Polygon
5. Creation of ArcMap Project (This file contains the results)

Enjoy it!



