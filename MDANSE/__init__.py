#MDANSE : Molecular Dynamics Analysis for Neutron Scattering Experiments
#------------------------------------------------------------------------------------------
#Copyright (C)
#2015- Eric C. Pellegrini Institut Laue-Langevin
#BP 156
#6, rue Jules Horowitz
#38042 Grenoble Cedex 9
#France
#pellegrini[at]ill.fr
#goret[at]ill.fr
#aoun[at]ill.fr
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 
'''
Created on Mar 26, 2015

@author: Eric C. Pellegrini
'''

from __pkginfo__ import __version__, __author__, __date__

from MDANSE.Core.Platform import PLATFORM
from MDANSE.Core.ClassRegistry import ClassRegistry as REGISTRY
from MDANSE.Core.MMTKDefinitions import MMTK_DEFINITIONS
from MDANSE.Core.UserDefinitions import USER_DEFINITIONS

from MDANSE.Data.ElementsDatabase import ELEMENTS

from MDANSE.Logging.Logger import LOGGER

import MDANSE.Framework
del MDANSE.Framework
