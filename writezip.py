#!/usr/bin/env python
import os
import zipfile

getCurrntPath = os.getcwd()
zipName = "/tmp/myzipfile.zip"
zf = zipfile.ZipFile(zipName, "w")
for dirname, subdirs, files in os.walk(getCurrntPath):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
print "Zip Converted Done........!!!"        
zf.close()



print "Zipped Fileunzip inprocess"
with zipfile.ZipFile(zipName,"r") as zip_ref:
        zip_ref.extractall("/tmp/")

print("ZipFile to UnZipped process Completed")








  
   
    
