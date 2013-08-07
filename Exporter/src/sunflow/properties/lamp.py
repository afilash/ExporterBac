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
# Created on                          07-Aug-2013
# Author                              NodeBench
# --------------------------------------------------------------------------


from .. import SunflowAddon

from extensions_framework import declarative_property_group
from extensions_framework.validate import Logic_Operator, Logic_OR as LOR

@SunflowAddon.addon_register_class
class sunflow_lamp(declarative_property_group):
    ef_attach_to = ['Lamp']
    
    controls = [
            'lightRadiance',
            'lightSamples',
            'lightShericalRadius',
            'lightSunExtend',
    ]
    
    visibility = {}
    
    properties = [
        
        {
            'type': 'int',
            'attr': 'lightSamples',
            'name': 'Samples',
            'description': 'The number of samples used to calculate the irradiance (default 64). ',            
            'min': 0,
            'max':   8192,
            'default': 64,
            'save_in_preset': True
        },
        {
            'type': 'float',
            'attr': 'lightShericalRadius',
            'name': 'Sherical Radius',
            'description': 'Radius of the sphere light (default 10.0).',
            'default': 10.0,
            'min': 0.0,
            'max': 10000.0,
            'save_in_preset': True
        },
        {
            'type': 'float',
            'attr': 'lightRadiance',
            'name': 'Radiance',
            'description': 'Specifies the intensity of the light source',
            'default': 10.0,
            'min': 0.0,
            'soft_min': 1e-3,
            'max': 1e5,
            'soft_max': 1e5,
            'save_in_preset': True
        },
        {
            'type': 'bool',
            'attr': 'lightSunExtend',
            'name': 'Extend Sun Sky',
            'description': 'Extend sun sky upto infenity (default False).',
            'default': False,
            'save_in_preset': True
        },
                  
    ] 
    
    mapping =  [
                ('point', 'point', 'light mapped to blender point type'),
                ('meshlight', 'mesh', 'light mapped to blender mesh (see material tab)'),
                ('spherical', 'hemi', 'light mapped to blender hemi type'),
                ('directional', 'spot', 'light mapped to blender spot type'),
                ('ibl', 'world_texture', 'light mapped to blender world type'),
                ('sunsky', 'sun', 'light mapped to blender sun type'),
                ('area', 'area', 'light mapped to blender area type')
            ]
    
    
    
if __name__ == '__main__':
    pass