# Map Photos

This script/tool will extract the photos from the attachments in a File Geodatabase and then use the Geotagged Photos to Points tool to map the points.

This will map the various photos taken by [Survey123 for ArcGIS](https://survey123.arcgis.com) or other collection tools

Input Parameters:
1. Input file geodatabase - the fiel geodatabase with the attachments
2. Output location - geodatabase or feature dataset you want to place the points in (for feature dataset, use 4326 as teh spatial reference)
3. Photo directory (optional) - the directory to write the photos out to; if not provided, this will be a temporoary directory deleted upon completion

Output Parameters:
4. The output location
5. The output feature classes (multi-value) 
