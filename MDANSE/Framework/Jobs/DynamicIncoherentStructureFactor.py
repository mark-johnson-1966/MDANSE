import collections

import numpy

from MDANSE import ELEMENTS, REGISTRY
from MDANSE.Framework.Jobs.IJob import IJob
from MDANSE.Mathematics.Arithmetic import weight
from MDANSE.Mathematics.Signal import correlation, get_spectrum
from MDANSE.MolecularDynamics.Trajectory import read_atoms_trajectory

class DynamicIncoherentStructureFactor(IJob):
    """
    Computes the dynamic incoherent structure factor for a set of atoms.
    """

    type = 'disf'
    
    label = "Dynamic Incoherent Structure Factor"

    category = ('Scattering',)
    
    ancestor = "mmtk_trajectory"
    
    configurators = collections.OrderedDict()
    configurators['trajectory']=('mmtk_trajectory',{})
    configurators['frames']=('frames', {"dependencies":{'trajectory':'trajectory'}})
    configurators['instrument_resolution'] = ('instrument_resolution',{"dependencies":{'trajectory':'trajectory', 'frames' : 'frames'}})
    configurators['q_vectors'] = ('q_vectors',{"dependencies":{'trajectory':'trajectory'}})
    configurators['atom_selection']=('atom_selection',{"dependencies":{'trajectory':'trajectory','grouping_level':'grouping_level'}})
    configurators['grouping_level']=('grouping_level',{})
    configurators['transmutated_atoms']=('atom_transmutation',{"dependencies":{'trajectory':'trajectory', 'atom_selection':'atom_selection'}})
    configurators['projection']=('projection', {"label":"project coordinates"})
    configurators['weights']=('weights',{"default" : "b_incoherent"})
    configurators['output_files']=('output_files', {"formats":["netcdf","ascii"]})
    configurators['running_mode']=('running_mode',{})
                    
    def initialize(self):
        """
        Initialize the input parameters and analysis self variables
        """

        self.numberOfSteps = self.configuration['atom_selection']['n_groups']

        self._nQShells = self.configuration["q_vectors"]["n_shells"]

        self._nFrames = self.configuration['frames']['number']
        
        self._instrResolution = self.configuration["instrument_resolution"]
        
        self._nFrequencies = self._instrResolution['n_frequencies']

        self._outputData.add("q","line", self.configuration["q_vectors"]["shells"], "q", units="inv_nm") 

        self._outputData["time"] = REGISTRY["output_variable"]("line", self.configuration['frames']['time'], "time", units='ps')
        self._outputData["time_window"] = REGISTRY["output_variable"]("line", self._instrResolution["time_window"], "time_window", axis="time", units="au") 

        self._outputData["frequency"] = REGISTRY["output_variable"]("line", self._instrResolution["frequencies"], "frequency", units='THz')
        self._outputData["frequency_window"] = REGISTRY["output_variable"]("line", self._instrResolution["frequency_window"], "frequency_window", axis="frequency", units="au") 
                        
        for element in self.configuration['atom_selection']['contents'].keys():
            self._outputData["f(q,t)_%s" % element] = REGISTRY["output_variable"]("surface", (self._nQShells,self._nFrames)     , "f(q,t)_%s" % element, axis="q|time", units="au")                                                 
            self._outputData["s(q,f)_%s" % element] = REGISTRY["output_variable"]("surface", (self._nQShells,self._nFrequencies), "s(q,f)_%s" % element, axis="q|frequency", units="nm2/ps") 

        self._outputData["f(q,t)_total"] = REGISTRY["output_variable"]("surface", (self._nQShells,self._nFrames)     , "f(q,t)_total", axis="q|time", units="au")                                                 
        self._outputData["s(q,f)_total"] = REGISTRY["output_variable"]("surface", (self._nQShells,self._nFrequencies), "s(q,f)_total", axis="q|frequency", units="nm2/ps") 
    
    def run_step(self, index):
        """
        Runs a single step of the job.\n
 
        :Parameters:
            #. index (int): The index of the step.
        :Returns:
            #. index (int): The index of the step. 
            #. atomicSF (numpy.array): The atomic structure factor
        """
        
        # get atom index
        indexes = self.configuration['atom_selection']["groups"][index]                                                                          
                
        series = read_atoms_trajectory(self.configuration["trajectory"]["instance"],
                                       indexes,
                                       first=self.configuration['frames']['first'],
                                       last=self.configuration['frames']['last']+1,
                                       step=self.configuration['frames']['step'])
        
        series = self.configuration['projection']["projector"](series)

        atomicSF = numpy.zeros((self._nQShells,self._nFrames), dtype=numpy.float64)

        for i,q in enumerate(self.configuration["q_vectors"]["shells"]):
                        
            if not q in self.configuration["q_vectors"]["value"]:
                continue
            
            qVectors = self.configuration["q_vectors"]["value"][q]["q_vectors"]
                        
            rho = numpy.exp(1j*numpy.dot(series, qVectors))
            res = correlation(rho, axis=0, average=1)
            
            atomicSF[i,:] += res
        
        return index, atomicSF
    
    
    def combine(self, index, x):
        """
        Combines returned results of run_step.\n
        :Parameters:
            #. index (int): The index of the step.\n
            #. x (any): The returned result(s) of run_step
        """
                
        # The symbol of the atom.
        element = self.configuration['atom_selection']['elements'][index][0]
        
        self._outputData["f(q,t)_%s" % element] += x
            
    
    def finalize(self):
        """
        Finalizes the calculations (e.g. averaging the total term, output files creations ...)
        """
        
        for element, number in self.configuration['atom_selection']['n_atoms_per_element'].items():
            self._outputData["f(q,t)_%s" % element][:] /= number
            self._outputData["s(q,f)_%s" % element][:] = get_spectrum(self._outputData["f(q,t)_%s" % element],
                                                                      self.configuration["instrument_resolution"]["time_window"],
                                                                      self.configuration["instrument_resolution"]["time_step"],
                                                                      axis=1)

        props = dict([[k,ELEMENTS[k,self.configuration["weights"]["property"]]] for k in self.configuration['atom_selection']['n_atoms_per_element'].keys()])
        
        self._outputData["f(q,t)_total"][:] = weight(props,self._outputData,self.configuration['atom_selection']['n_atoms_per_element'],1,"f(q,t)_%s")
        
        self._outputData["s(q,f)_total"][:] = weight(props,self._outputData,self.configuration['atom_selection']['n_atoms_per_element'],1,"s(q,f)_%s")
    
        self._outputData.write(self.configuration['output_files']['root'], self.configuration['output_files']['formats'], self.header)
        
        self.configuration['trajectory']['instance'].close()