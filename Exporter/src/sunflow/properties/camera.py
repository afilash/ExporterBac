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
# Created on                          04-Aug-2013
# Author                              NodeBench
# --------------------------------------------------------------------------


from .. import SunflowAddon

from extensions_framework import declarative_property_group
from extensions_framework import util as efutil


@SunflowAddon.addon_register_class
class sunflow_film(declarative_property_group):
    """ Properties for controlling the output file format currently (0.7.3) 
    supports only 4 file formats PNG, HDR, TARGA, OpenEXR. when render through 
    GUI, it only supports PNG output All other four formats are generated 
    through using command line arguments.       
        -nogui -o output.tga scenefile.sc
            
    """

    ef_attach_to = ['Camera']
    controls = []
    visibility = {}
    enabled = {}
    alert = {}
    
    
    def set_extension(self, context):
        if self.fileFormat == 'png':
            self.fileExtension = 'png'
        elif self.fileFormat == 'openexr':
            self.fileExtension = 'exr'
        elif self.fileFormat == 'hdr':
            self.fileExtension = 'hdr'
        elif self.fileFormat == 'targa':
            self.fileExtension = 'tga'
        else:
            self.fileExtension = ''
    
    properties = [
        {
            'type': 'string',
            'attr': 'fileExtension',
            'name': 'File Extension',
            'default': 'png',
            'save_in_preset': True
        },
        {
            'type': 'enum',
            'attr': 'fileFormat',
            'name': 'File Format',
            'description': 'Denotes sunflow film output file format (default PNG)',
            'items': [
                ('png', 'PNG', 'png'),
                ('hdr', 'HDR', 'hdr (only supported on command line mode)'),
                ('openexr', 'OpenEXR', 'openexr (only supported on command line mode)'),
                ('targa', 'Targa', 'targa (only supported on command line mode)')
            ],
            'default': 'png',
            'update': set_extension,
            'save_in_preset': True
        },
                  ]
    
