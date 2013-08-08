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
# Created on                          08-Aug-2013
# Author                              NodeBench
# --------------------------------------------------------------------------

import bpy, bl_ui

from .. import SunflowAddon

from extensions_framework import declarative_property_group
from extensions_framework.validate import Logic_Operator, Logic_OR as LOR

@SunflowAddon.addon_register_class
class sunflow_material(declarative_property_group):
    ef_attach_to = ['Material']
    
    controls = [
            'type',
    ]
    
    visibility = {}
    
    properties = [
        {
            'type': 'enum',
            'attr': 'type',
            'name': 'Type',
            'description': 'Specifes the type of sunflow material',
            'items': [
                ('constant','constant','Constant (surface variation wont be considered).'),
                ('diffuse','Diffuse','Diffuse (Plain diffuse shader).'),
                ('phong','Phong','Phong'),
                ('shiny','Shiny','Shiny'),
                ('glass','Glass','Glass'),
                ('mirror','Mirror','Mirror'),
                ('ward','Ward','Ward'),
                ('ambientocclusion','Ambient Occlusion','Ambient Occlusion'),
                ('uber','Uber','Uber (Diffuse ,Specular mix shader)'),
                ('janino','Janino','Janino (Java compile time shader)'),
                ('light','Light','Light (if applied to an object , that object will be converted as a mesh light).'),
                ('none', 'Passthrough material', 'none (means this object will not be rendered).')
            ],
            'default': 'diffuse',
            'save_in_preset': True
        }
                                   
    ] 
    
   
if __name__ == '__main__':
    pass