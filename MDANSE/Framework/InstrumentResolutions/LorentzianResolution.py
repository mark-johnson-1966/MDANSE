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
Created on Mar 30, 2015

@author: pellegrini
'''

import numpy

from MDANSE.Framework.Configurators.ConfiguratorsDict import ConfiguratorsDict
from MDANSE.Framework.InstrumentResolutions.IInstrumentResolution import IInstrumentResolution
                 
class LorentzianInstrumentResolution(IInstrumentResolution):
    """
    Defines an instrument resolution with a lorentzian response
    """
    
    type = 'lorentzian'

    configurators = ConfiguratorsDict()
    configurators.add_item('mu', 'float', default=0.0)
    configurators.add_item('sigma', 'float', default=1.0)

    __doc__ += configurators.build_doc()

    def set_kernel(self, frequencies, dt):

        mu = self._configuration["mu"]["value"]
        sigma = self._configuration["sigma"]["value"]
                
        fact = 0.5*sigma
                          
        self._frequencyWindow = (1.0/numpy.pi)*(fact/((frequencies-mu)**2 + fact**2))
                
        self._timeWindow = numpy.fft.fftshift(numpy.abs(numpy.fft.ifft(self._frequencyWindow))/dt)