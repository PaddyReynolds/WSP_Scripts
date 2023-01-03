#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     07/12/2022
# Copyright:   (c) UKPXR011 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
from os import listdir
from os.path import isfile, join

Folder = r'C:\Users\UKPXR011\Desktop\Scripts\Dave_Rename'

Suffix = 'Fuck_Off_Dave'

def append_id(filename):
    name, ext = os.path.splitext(filename)
    return "{name}_{uid}{ext}".format(name=name, uid=Suffix, ext=ext)


onlyfiles = [f for f in listdir(Folder) if isfile(join(Folder, f))]

for filename in onlyfiles:
    print 'Renaming ' + filename
    old_Name_dir = Folder +'\\' + filename
    new_name = append_id(filename)
    new_name_dir = Folder + '\\'+ new_name
    #print new_name_dir, old_Name_dir
    os.rename(old_Name_dir,new_name_dir)

os.rename