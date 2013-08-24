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
# Created on                          23-Aug-2013
# Author                              NodeBench
# --------------------------------------------------------------------------


def getPos(obj , as_matrix=True):
    obj_mat = obj.matrix.copy()
    matrix_rows = [ "%+0.4f" % element for rows in obj_mat for element in rows ]
    return (matrix_rows)


def ParticleInstancing(scene , objname , motion_blur , mblur_steps):
    
    if not motion_blur:
        print('no mblur')
        dupli_list = {}
        
        obj = scene.objects[objname]
        if not hasattr(obj, 'modifiers'):
            print('no attr modifi')
            return dupli_list
        
        for mod in obj.modifiers :
            print(mod.type)
            if mod.type == 'PARTICLE_SYSTEM':
                psys = mod.particle_system
                if psys.settings.type != 'HAIR':
                    print('not hair')
                    continue
                if psys.settings.render_type not in ['OBJECT', 'GROUP']:
                    print(psys.settings.render_type)
                    continue                
                
                obj.dupli_list_create(scene)
                for ob in obj.dupli_list:
                    if ob.hide :
                        print('hide')
                        continue
                    ins = {}  
                    pos = getPos(ob, as_matrix=True) 
                    ins['iname'] = "%s.inst.%03d" % (obj.name, ob.index)
                    ins['index'] = ob.index
                    ins['pname'] = ob.object.name
                    ins['trans'] = [pos]
                    dupli_list[ ins['iname'] ] = ins
                obj.dupli_list_clear()
        return dupli_list
                    
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
