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

from extensions_framework.ui import property_group_renderer
from extensions_framework import util as efutil


class sunflow_material_base(bl_ui.properties_material.MaterialButtonsPanel, property_group_renderer):
    COMPAT_ENGINES    = { 'SUNFLOW_RENDER' }
    
    def draw(self, context):
        if not hasattr(context, 'material'):
            return
        return super().draw(context)



@SunflowAddon.addon_register_class
class MATERIAL_PT_material(sunflow_material_base, bpy.types.Panel):
    '''
    Material UI Panel
    '''
    
    bl_label    = 'Sunflow Material'
    COMPAT_ENGINES    = { 'SUNFLOW_RENDER' }
    
    display_property_groups = [
        ( ('material',), 'sunflow_material' )
    ]
    

    
    def draw(self, context):
        layout = self.layout
        mat = context.material.sunflow_material
        #layout.active = (mat.use_bsdf)
        layout.prop(context.material.sunflow_material, "type", text="")
#        if mat.type != 'none':
#            bsdf = getattr(mat, 'mitsuba_bsdf_%s' % mat.type)
#            for p in bsdf.controls:
#                self.draw_column(p, self.layout, mat, context,
#                    property_group=bsdf)
#            bsdf.draw_callback(context)
        

if __name__ == '__main__':
    pass