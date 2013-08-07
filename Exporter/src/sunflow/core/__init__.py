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


from ..properties import (camera , render , integrator , lamp)

#from ..properties import (
#    engine, sampler, , lamp, texture,
#    material, mesh, , world
#)
#





from ..ui import (camera , render , lamps)

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


def _register_elm(elm, required=False):
    try:
        elm.COMPAT_ENGINES.add('SUNFLOW_RENDER')
    except:
        pass

def compatible(mod):
    mod = getattr(bl_ui, mod)
    for subclass in mod.__dict__.values():
        _register_elm(subclass)
    del mod
    

# Add standard Blender Interface elements
_register_elm(bl_ui.properties_render.RENDER_PT_render, required=True)
_register_elm(bl_ui.properties_render.RENDER_PT_dimensions, required=True)

_register_elm(bl_ui.properties_scene.SCENE_PT_scene, required=True)
_register_elm(bl_ui.properties_scene.SCENE_PT_audio)
_register_elm(bl_ui.properties_scene.SCENE_PT_physics) #This is the gravity panel
_register_elm(bl_ui.properties_scene.SCENE_PT_keying_sets)
_register_elm(bl_ui.properties_scene.SCENE_PT_keying_set_paths)
_register_elm(bl_ui.properties_scene.SCENE_PT_unit)
_register_elm(bl_ui.properties_scene.SCENE_PT_color_management)
_register_elm(bl_ui.properties_scene.SCENE_PT_rigid_body_world)
_register_elm(bl_ui.properties_scene.SCENE_PT_custom_props)

_register_elm(bl_ui.properties_world.WORLD_PT_context_world, required=True)

_register_elm(bl_ui.properties_material.MATERIAL_PT_preview)
_register_elm(bl_ui.properties_texture.TEXTURE_PT_preview)

_register_elm(bl_ui.properties_data_lamp.DATA_PT_context_lamp)
    
_register_elm(bl_ui.properties_data_camera.DATA_PT_context_camera)
_register_elm(bl_ui.properties_data_camera.DATA_PT_lens)
_register_elm(bl_ui.properties_data_camera.DATA_PT_camera)
_register_elm(bl_ui.properties_data_camera.DATA_PT_camera_display)
_register_elm(bl_ui.properties_data_camera.DATA_PT_custom_props_camera)





# DEFAULT PANELS
compatible("properties_data_mesh")
#compatible("properties_data_camera")
compatible("properties_particle")
compatible("properties_data_speaker")    
    
    

@SunflowAddon.addon_register_class
class RENDERENGINE_sunflow(bpy.types.RenderEngine):
    bl_idname           = 'SUNFLOW_RENDER'
    bl_label            = 'Sunflow'
    bl_use_preview      = True
  
  
    def render(self, scene):
        print("Press RENDER")



if __name__ == '__main__':
    pass