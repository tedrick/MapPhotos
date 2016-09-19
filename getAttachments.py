#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jame6423
#
# Created:     13/09/2016
# Copyright:   (c) jame6423 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os, tempfile, shutil
import arcpy

def getAttachmentTables(workspace):
    '''Lists the tables that have attachments'''
    arcpy.AddMessage('\t-Finding Attachments')
    originalWorkspace = arcpy.env.workspace
    arcpy.env.workspace = workspace
    dscW = arcpy.Describe(workspace)
    tableList = []
    relClasses = [c.name for c in dscW.children if c.datatype == u'RelationshipClass']
    for child in relClasses:
        dscRC = arcpy.Describe(child)
        if dscRC.isAttachmentRelationship:
            destTable = dscRC.destinationClassNames[0]
            destParts = destTable.split(".")
            tableList.append(destParts[-1])
    arcpy.env.workspace = originalWorkspace
    return tableList

def exportAttachments(workspace, table, outLocation):
    originalWorkspace = arcpy.env.workspace
    arcpy.env.workspace = workspace
    '''For a given attachment table, export the files to the directory specified'''
    with arcpy.da.SearchCursor(table, ['DATA', 'ATT_NAME', 'ATTACHMENTID']) as cursor:
        for item in cursor:
            attachment = item[0]
            filenum = "ATT" + str(item[2]) + "_"
            filename = filenum + str(item[1])
            open(outLocation + os.sep + filename, 'wb').write(attachment.tobytes())
            del item
            del filenum
            del filename
            del attachment
    arcpy.env.workspace = originalWorkspace

def main():
    inFGDB = arcpy.GetParameterAsText(0)
    outLocation = arcpy.GetParameterAsText(1)
    photoDir = arcpy.GetParameterAsText(2)

    deleteDirectory = False
    if photoDir == "":
        photoDir = tempfile.mkdtemp()
        deleteDirectory = True

    attachmentTables = getAttachmentTables(inFGDB)

    outFCList = []
    for table in attachmentTables:
        tablename = table.replace('__ATTACH','')
#        tablename = tablename.strip('_')
        tabledir = os.path.join(photoDir, tablename)
        os.mkdir(tabledir)
        exportAttachments(inFGDB, table, tabledir)
        photo_Prefix = tablename
        photoTable = photo_Prefix + "_PHOTOS"
        photosFC = os.path.join(outLocation, photoTable)
        arcpy.GeoTaggedPhotosToPoints_management(tabledir, photosFC, Add_Photos_As_Attachments="ADD_ATTACHMENTS")
        outFCList.append(photosFC)

    outFGDB = arcpy.SetParameterAsText(3, outLocation)
    outFCs =  arcpy.SetParameterAsText(4, ';'.join(outFCList))

    if deleteDirectory == True:
        shutil.rmtree(photoDir, ignore_errors=True)

    return

if __name__ == '__main__':
    main()
