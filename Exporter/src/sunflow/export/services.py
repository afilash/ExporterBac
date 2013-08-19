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
# Created on                          18-Aug-2013
# Author                              NodeBench
# --------------------------------------------------------------------------



import os
import copy
# Framework libs
from extensions_framework import util as efutil


def mix(MasterDict, InputDict , TargetName):
    for keys in InputDict.keys():
        if keys not in MasterDict.keys():
            MasterDict[keys] = {}
        if InputDict[keys] != []:
            MasterDict[keys][TargetName] = InputDict[keys]


def tr_color_str(_color):
    colors = [ "%+0.4f" % channel for channel in _color ]
    return '  '.join(colors)

        
def make_path_real(path):
    xfac = efutil.filesystem_path(path)
    return os.path.abspath(xfac)


def file_exists(filepath):
    path = make_path_real(filepath)
    if os.path.exists(path):
        return True
    else:
        return False
    

def getObjectPos(obj, as_matrix=True):
    obj_mat = obj.matrix_world.copy()
    if not as_matrix :
        obj_mat.transpose()
        eye = obj_mat[3]
        dir = obj_mat[2]
        up = obj_mat[1]
        target = eye - dir        
        points = [ eye.to_tuple()[:3], target.to_tuple()[:3], up.to_tuple()[:3] ]        
        pos = [ "%+0.4f %+0.4f %+0.4f" % elm for elm in points ]
        return (pos)
    else:
        matrix_rows = [ "%+0.4f" % element for rows in obj_mat for element in rows ]
        return (matrix_rows)
            
def dict_merge(*dictionaries):
    cp = {}
    for dic in dictionaries:
        cp.update(copy.deepcopy(dic))
    return cp

def dmix(MasterDict, InputDict , TargetName):
    if TargetName not in MasterDict.keys():
        MasterDict[TargetName] = {}        
    for keys in InputDict.keys():
        MasterDict[TargetName][keys] = InputDict[keys]