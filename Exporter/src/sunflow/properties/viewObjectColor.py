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


def change_diffuse_color(self , context):
    if context.object.active_material is not None:
        if self.type == 'diffuse':
            context.object.active_material.diffuse_color = self.diffuseColor.copy()
            context.object.active_material.specular_color = (0.0, 0.0, 0.0)
        elif self.type == 'constant':            
            context.object.active_material.diffuse_color = self.constantColor.copy()
            context.object.active_material.specular_color = (0.0, 0.0, 0.0)
            context.object.active_material.emit = self.constantEmit
        elif self.type == 'phong':                   
            context.object.active_material.diffuse_color = self.phongColor.copy()
            context.object.active_material.specular_color = self.phongSpecular.copy()
            context.object.active_material.specular_hardness = self.phongSpecHardness
        elif self.type == 'shiny':                   
            context.object.active_material.diffuse_color = self.shinyDiffuse.copy()
            context.object.active_material.specular_color = (0.0, 0.0, 0.0)
        else:
            pass
        
            


if __name__ == '__main__':
    pass