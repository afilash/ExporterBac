# -*- coding: utf8 -*-
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# ***** END GPL LICENCE BLOCK *****
#
# --------------------------------------------------------------------------
# Blender Version                     2.68
# Exporter Version                    0.0.1
# Created on                          21-Jul-2013
# Author                              NodeBench
# --------------------------------------------------------------------------


import os
import shutil
import subprocess



BLENDER_PATH= "E:\\Graphics\\BlenderFoundation\\blender-2.68-RC1-windows32\\blender.exe"
FILE_PATH = "E:\\DevelProjects\\gitRepository\\sfrsTest\\sfrsTest\\src\\blends\\casestudies\\testblender.blend"



def copyroot():
    dest_dir =r"C:\Users\AppleCart\AppData\Roaming\Blender Foundation\Blender\2.67\scripts\addons\sunflow"
    source_dir = r"./sunflow"
    
    #----------------------------------------------------------- print os.curdir
    #---------------------------------------------- print os.listdir(source_dir)
    #--------------------------------------------- shutil.rmtree(path=dest_dir )
    #------------------------------------- shutil.copytree(source_dir, dest_dir)
    
    
    print ("Current directory  %s"  %(os.curdir))
    print ("Removing directory %s"  %(dest_dir))
    if os.path.exists(dest_dir):
        shutil.rmtree(path=dest_dir )
    print ("Copying directory  %s"  %(source_dir))
    shutil.copytree(source_dir, dest_dir)
    
    print("Copy Done!")
    
    subprocess.call([BLENDER_PATH,FILE_PATH])
    
    print ("Finished!")
    
    
def pathprt():
    print os.curdir
    print os.listdir(".")

if __name__ == '__main__':
    copyroot()
#    pathprt()