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

Folder = r'C:\Users\UKPXR011\Desktop\Scripts\Dave_Rename'

Suffix = 'Fuck_Off_Dave'

def append_id(filename):
    name, ext = os.path.splitext(filename)
    return "{name}_{uid}{ext}".format(name=name, uid=Suffix, ext=ext)


for filename in os.listdir(Folder):
    print 'Renaming ' + filename
    old_Name_dir = Folder +'\\' + filename
    new_name = append_id(filename)
    new_name_dir = Folder + '\\'+ new_name
    #print new_name_dir, old_Name_dir
    os.rename(old_Name_dir,new_name_dir)

os.rename