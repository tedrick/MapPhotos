
# coding: utf-8

# Load the classes used
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection


# Logging in with my username and password, replace with your own
import getpass
password = getpass.getpass("Enter password: ")
gis = GIS("https://www.arcgis.com","jtedrick_melbournedev", password)

#Looking for the layer to download via search; this is a search that returns one item
layerSearch = gis.content.search(query="EXIF", item_type="Feature Layer")
exportLayer = FeatureLayerCollection.fromitem(layerSearch[0])

# The exportLayer item has 2 things to check for attachments - the layers and the tables

for lyr in exportLayer.layers:
    if lyr.attachments:
        query_features = lyr.query(where='1=1')
        oidField = query_features.object_id_field_name
        for f in query_features.features:
            f_id = f.get_value(oidField)
            attach_list = lyr.attachments.get_list(oid=f_id)
            for attach in attach_list:
                attach_id = attach['id']
                lyr.attachments.download(oid=f_id, attachment_id=attach_id, save_path="/Users/jame6423/temp/attach")

for tbl in exportLayer.tables:
    if tbl.attachments:
        query_features = tbl.query(where='1=1')
        oidField = query_features.object_id_field_name
        for f in query_features.features:
            f_id = f.get_value(oidField)
            attach_list = tbl.attachments.get_list(oid=f_id)
            for attach in attach_list:
                attach_id = attach['id']
                tbl.attachments.download(oid=f_id, attachment_id=attach_id, save_path="/Users/jame6423/temp/attach")
