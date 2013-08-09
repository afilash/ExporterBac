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
# Created on                          09-Aug-2013
# Author                              NodeBench
# --------------------------------------------------------------------------


import bpy, bl_ui

from .. import SunflowAddon

from extensions_framework.ui import property_group_renderer

narrowui = 180

class sunflow_rlayers(bl_ui.properties_render_layer.RenderLayerButtonsPanel, property_group_renderer):
    COMPAT_ENGINES = { 'SUNFLOW_RENDER' }

@SunflowAddon.addon_register_class
class sunflow_rlayers_panel(sunflow_rlayers):
    bl_label = 'Sunflow Rlayes'
    
    display_property_groups = [
        ( ('scene',), 'sunflow_renderlayercfg' )
    ]
    
    # Overridden to draw some of blender's lamp controls
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop( context.scene.sunflow_renderlayercfg ,"examPath")
            