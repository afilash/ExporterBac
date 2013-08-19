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

# TODO sfrsFilmDisplay
from ..outputs import sunflowLog , sunflowFilmDisplay
from ..export import (getExporter)



# from ..export.scene import SceneExporter
#


from ..properties import (camera , render , integrator , lamp , materials , renderlayers , world)

# from ..properties import (
#    engine, sampler, , lamp, texture,
#    material, mesh, , world
# )
#





from ..ui import (camera , render , lamps , materials , renderlayers , world)

# from ..ui import (
#    render, render_layer, lamps, materials, mesh, 
#    camera, world
# )
#


# from ..ui.materials import (
#    main, subsurface, medium, emitter
# )
#

from .. import operators



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
_register_elm(bl_ui.properties_scene.SCENE_PT_physics)  # This is the gravity panel
_register_elm(bl_ui.properties_scene.SCENE_PT_keying_sets)
_register_elm(bl_ui.properties_scene.SCENE_PT_keying_set_paths)
_register_elm(bl_ui.properties_scene.SCENE_PT_unit)
_register_elm(bl_ui.properties_scene.SCENE_PT_color_management)
_register_elm(bl_ui.properties_scene.SCENE_PT_rigid_body_world)
_register_elm(bl_ui.properties_scene.SCENE_PT_custom_props)

_register_elm(bl_ui.properties_world.WORLD_PT_context_world, required=True)
_register_elm(bl_ui.properties_world.WORLD_PT_preview, required=True)
_register_elm(bl_ui.properties_world.WORLD_PT_world, required=True)


_register_elm(bl_ui.properties_material.MATERIAL_PT_context_material)
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
compatible("properties_texture")
# compatible("properties_data_camera")
compatible("properties_particle")
compatible("properties_data_speaker")
    
    

@SunflowAddon.addon_register_class
class RENDERENGINE_sunflow(bpy.types.RenderEngine):
    bl_idname = 'SUNFLOW_RENDER'
    bl_label = 'Sunflow'
    bl_use_preview = True
  
  

    render_lock = threading.Lock()
    

    def render(self, scene):

        if self is None or scene is None:
            print('ERROR: Scene is missing!')
            return
        
        with self.render_lock:  # just render one thing at a time
            if scene.name == 'preview':
                self.render_preview(scene)
                return

            print(self.is_animation)
                        
            scene_path = efutil.filesystem_path(scene.render.filepath)
            if os.path.isdir(scene_path):
                output_dir = scene_path
            else:
                output_dir = os.path.dirname(scene_path)        
            
            output_dir = os.path.abspath(os.path.join(output_dir , efutil.scene_filename()))            
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            # print('Sunflow: Current directory = "%s"' % output_dir)
            
            if not getExporter (output_dir, scene.name, scene.frame_current):
                return 
            
            if self.is_animation:
                return
            
            arguments = self.getCommandLineArgs(scene)
            
            
                    
            
            jarpath = efutil.find_config_value('sunflow', 'defaults', 'jar_path', '')
            javapath = efutil.find_config_value('sunflow', 'defaults', 'java_path', '')
            memory = "-Xmx%sm" % efutil.find_config_value('sunflow', 'defaults', 'memoryalloc', '')
            image_name = "%s.%03d.%s" % (scene.name , scene.frame_current, arguments['format'])
            sunflow_file = "%s.%03d.sc" % (scene.name , scene.frame_current)
            image_file = os.path.abspath(os.path.join(output_dir , image_name))
            sc_file_path = os.path.abspath(os.path.join(output_dir , sunflow_file))
            
            cmd_line = [ javapath , memory , '-server' , '-jar' , jarpath ]
            final_line = ['-o', image_file , sc_file_path]     
            
            extra = []
            for key in arguments:
                if key == 'format':
                    continue
                if arguments[key] != '':
                    values = arguments[key].split()
                    print(values)
                    extra.extend(values)
            
            if arguments['format'] != 'png':
                extra.append('-nogui')
            
            cmd_line.extend(extra)
            cmd_line.extend(final_line)
            print(cmd_line)
            subprocess.Popen(cmd_line)


    def render_preview(self, scene):
        print("Render Preview Initiated")
    
    
        
    
    def getCommandLineArgs(self , scene):
        argument = {}
        quickmappings = {
                        'quicknone': '',
                        'quickuvs': '-quick_uvs',
                        'quicknormals': '-quick_normals',
                        'quickid': '-quick_id',
                        'quickprims': '-quick_prims',
                        'quickgray': '-quick_gray',
                        'quickwire': '-quick_wire',
                        'quickambocc': '-quick_ambocc'  ,
                         }
        if  scene.sunflow_passes.quickmode == 'quickwire':
            extra = " -aa %s %s -filter %s " % (scene.sunflow_antialiasing.adaptiveAAMin , scene.sunflow_antialiasing.adaptiveAAMax, scene.sunflow_antialiasing.imageFilter)
        elif scene.sunflow_passes.quickmode == 'quickambocc':
            extra = " %s " % scene.sunflow_passes.distOcclusion
        else:
            extra = ""        
        argument['quick'] = quickmappings[scene.sunflow_passes.quickmode] + extra
        
        if scene.render.threads_mode == 'FIXED':
            threads = "-threads %s" % scene.render.threads
        else:
            threads = ''       
        argument['threads'] = threads
        
    #     if scene.sunflow_performance.useCacheObjects:
    #         argument['usecache'] = True
    #     else:
    #         argument['usecache'] = False
            
        if scene.sunflow_performance.useSmallMesh:
            argument['smallmesh'] = '-smallmesh'
        else:
            argument['smallmesh'] = ''
            
        if scene.sunflow_performance.threadHighPriority  :
            argument['threadprio'] = '-hipri'
        else:
            argument['threadprio'] = ''
            
        if scene.sunflow_performance.enableVerbosity:
            argument['verbosity'] = '-v 4'
        else:
            argument['verbosity'] = ''
            
        if scene.sunflow_performance.ipr:
            argument['ipr'] = '-ipr'
        else:
            argument['ipr'] = ''
            
            
    #     if scene.render.use_instances:
    #         argument['useinstances'] = True
    #     else:
    #         argument['useinstances'] = False
    
        if getattr(scene , 'camera') is not None:
            argument['format'] = scene.camera.data.sunflow_film.fileExtension
        else:
            argument['format'] = 'png'
            
        
              
        return argument
        
            
            
