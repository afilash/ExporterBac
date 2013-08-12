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
# Created on                          22-Jul-2013
# Author                              NodeBench
# --------------------------------------------------------------------------
 
import os
import bpy
from extensions_framework import log
from extensions_framework.util import TimerThread

def sunflowLog(*args, popup=False):
    '''
    Send string to EF log, marked as belonging to sunflow module.
    Accepts variable args 
    '''
    if len(args) > 0:
        log(' '.join(['%s' % a for a in args]), module_name='sunflow', popup=popup)

class sunflowFilmDisplay(TimerThread):
    '''
    Periodically update render result with sunflow's framebuffer
    '''
    
    #===========================================================================
    # TODO
    # don't know how to implement in the current situation
    #===========================================================================
    pass
