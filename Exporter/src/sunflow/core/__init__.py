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
import os, time, threading, sys, copy, subprocess, random, ctypes

# Blender libs
import bpy, bl_ui

# Framework libs
from extensions_framework import util as efutil

from .. import SunflowAddon, plugin_path

# TODO sfrsFilmDisplay
from ..outputs import sunflowLog , sunflowFilmDisplay
from ..export import (getExporter)
from ..export.services import (resolution , get_instance_materials)
from ..export.shaders import create_shader_block


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
import shutil




# DEBUG = True
# if DEBUG:
#     import sys
#     sys.path.append(os.environ['PYDEV_DEBUG_PATH'])
#     import pydevd



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
        
        scene.render.use_placeholder = False
        
        with self.render_lock:  # just render one thing at a time
            if scene.name == 'preview':
                self.render_preview(scene)
                return

            # print(self.is_animation)
                        
            scene_path = efutil.filesystem_path(scene.render.filepath)
            if os.path.isdir(scene_path):
                output_dir = scene_path
            else:
                output_dir = os.path.dirname(scene_path)        
            
            output_dir = os.path.abspath(os.path.join(output_dir , efutil.scene_filename()))            
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            # print('Sunflow: Current directory = "%s"' % output_dir)
            
#             if DEBUG: pydevd.settrace()
            
            if not getExporter (output_dir, scene.name, scene.frame_current):
                return 
            
            if self.is_animation:
                return
            
            arguments = self.getCommandLineArgs(scene)
            
            
                    
            
            jarpath = efutil.find_config_value('sunflow', 'defaults', 'jar_path', '')
            javapath = efutil.find_config_value('sunflow', 'defaults', 'java_path', '')
            memory = "-Xmx%sm" % efutil.find_config_value('sunflow', 'defaults', 'memoryalloc', '')
            image_name = "%s.%03d.%s" % (scene.name , scene.frame_current, arguments['format'])
            if scene.sunflow_performance.useRandom:
                image_name = self.check_randomname(output_dir, image_name)
            
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
                    # print(values)
                    extra.extend(values)
            
            if arguments['format'] != 'png':
                extra.append('-nogui')
            
            cmd_line.extend(extra)
            cmd_line.extend(final_line)
            # print(cmd_line)
            subprocess.Popen(cmd_line)


    def convert_idiotic_path_names(self, path):
        tmp = path
        GetLongPathName = ctypes.windll.kernel32.GetLongPathNameW
        buffer = ctypes.create_unicode_buffer(GetLongPathName(tmp, 0, 0))
        GetLongPathName(tmp, buffer, len(buffer))
        # print(buffer.value)
        return buffer.value
    
    
    def render_preview(self, scene):
        (width, height) = resolution(scene)
        if (width < 96 or height < 96):
            return
        # print('Preview Render Res:  %s %s ' % (width, height))
    
        objects_materials = {}
        for object in [ob for ob in scene.objects if ob.is_visible(scene) and not ob.hide_render]:
            for mat in get_instance_materials(object):
                if mat is not None:
                    if not object.name in objects_materials.keys(): objects_materials[object] = []
                    objects_materials[object].append(mat)
        
        # find objects that are likely to be the preview objects
        preview_objects = [o for o in objects_materials.keys() if o.name.startswith('preview')]
        if len(preview_objects) < 1:
            return
        
        # find the materials attached to the likely preview object
        likely_materials = objects_materials[preview_objects[0]]
        if len(likely_materials) < 1:
            return
        
        tempdir = efutil.temp_directory()
        matfile = "ObjectMaterial.mat.sc"
        scenefile = "Scene.sc"
        outfile = "matpreview.png"
        output_file = [os.path.abspath(os.path.join(tempdir, scenefile)),
                       os.path.abspath(os.path.join(tempdir, outfile)),
                       os.path.abspath(os.path.join(tempdir, matfile)), ]     
        pm = likely_materials[0]
        # print(pm)
        mat_dic = create_shader_block(pm)
        linenum = 0 
        found = False
        if (('Shader' in mat_dic.keys()) and (len(mat_dic['Shader']) > 0)):
            for eachline in mat_dic['Shader']:
                if eachline.find(' name "') >= 0 :
                    found = True
                    break
                linenum += 1
        if not found:
            return
        matgot = mat_dic['Shader'][:]
        matgot[1] = '         name   "ObjectMaterial"'
        out_write = []
        out_write.append(' image {')
        out_write.append('resolution %s  %s' % (width, height))
        out_write.append('aa 0  1     samples 4     filter mitchell      jitter False       } ')
        out_write.extend(matgot)
        
        fi = open(output_file[2] , 'w')
        [ fi.write("\n%s " % line) for line in out_write]
        fi.close()
        src = os.path.join(plugin_path() , "preview", 'Scene.sc')
              
        shutil.copy(src, tempdir)
        
    
        jarpath = efutil.find_config_value('sunflow', 'defaults', 'jar_path', '')
        javapath = efutil.find_config_value('sunflow', 'defaults', 'java_path', '')
        memory = "-Xmx%sm" % efutil.find_config_value('sunflow', 'defaults', 'memoryalloc', '')
        
        cmd_line = [ javapath , memory , '-server' , '-jar' , jarpath , '-nogui', '-v', '0', '-o', output_file[1] , output_file[0]]     
        
        # print(cmd_line)
        
        
        sunflow_process = subprocess.Popen(cmd_line)

        framebuffer_thread = sunflowFilmDisplay()
        framebuffer_thread.set_kick_period(2) 
        framebuffer_thread.begin(self, output_file[1], resolution(scene))
        render_update_timer = None
        while sunflow_process.poll() == None and not self.test_break():
            render_update_timer = threading.Timer(1, self.process_wait_timer)
            render_update_timer.start()
            if render_update_timer.isAlive(): render_update_timer.join()
        
        # If we exit the wait loop (user cancelled) and mitsuba is still running, then send SIGINT
        if sunflow_process.poll() == None:
            # Use SIGTERM because that's the only one supported on Windows
            sunflow_process.send_signal(subprocess.signal.SIGTERM)
        
        # Stop updating the render result and load the final image
        framebuffer_thread.stop()
        framebuffer_thread.join()
        
        if sunflow_process.poll() != None and sunflow_process.returncode != 0:
            print("MtsBlend: Rendering failed -- check the console")
        else:
            framebuffer_thread.kick(render_end=True)
        framebuffer_thread.shutdown()
        
        
    def process_wait_timer(self):
        # Nothing to do here
        pass     
        
        
    def check_randomname(self , output_dir, image_name):
        new_name = image_name
        while (os.path.exists(os.path.join(output_dir, new_name))):
            num = str(random.randint(10000, 99999))
            tname = image_name.split('.')
            tname.insert(-1, num)
            new_name = '.'.join(tname)
        return new_name
        
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
        
            
            
