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
# Created on                          19-Jul-2013
# Author                              NodeBench
# --------------------------------------------------------------------------



# System libs
import os, time, threading, sys, copy, subprocess

# Blender libs
import bpy, bl_ui

# Framework libs
from extensions_framework import util as efutil

from .. import SunflowAddon, plugin_path

#TODO sfrsFilmDisplay
from ..outputs import sunflowLog , sunflowFilmDisplay

from ..export import (get_instance_materials, resolution, sunflowLaunch)



#from ..export.scene import SceneExporter
#

#from ..properties import (
#    engine, sampler, integrator, lamp, texture,
#    material, mesh, camera, world
#)
#

#from ..ui import (
#    render, render_layer, lamps, materials, mesh, 
#    camera, world
#)
#


#from ..ui.materials import (
#    main, subsurface, medium, emitter
#)
#

#from .. import operators
#



@SunflowAddon.addon_register_class
class RENDERENGINE_sunflow(bpy.types.RenderEngine):
    bl_idname           = 'SUNFLOW_RENDER'
    bl_label            = 'Sunflow'
    bl_use_preview      = True
  
  
    def render(self, scene):
        print("Press RENDER")



if __name__ == '__main__':
    pass