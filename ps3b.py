# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 
"""
Simulation of a population of viruses that can multiply, die and mutate over time. At any time interval, a virus has probability of producing its copy with same parameters as its own (resistance to each drug can switch from on to off and vice versa with some probability). This probability is computed from basic reproduction rate of this virus multiplied by percent of population avaliable to create out of maximum mossible population. It wont reproduce at all if it doesnt have resistances to all of the drugs active at that moment in simulation. Each virus at any time can alse die with certain probability. 
"""

import random
import pylab
import string
#from ps3b_precompiled_311 import *



class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """



#
# PROBLEM 1
#
class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        if random.random() < self.getClearProb():
            return True
        else:
            return False

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        birthProb = self.getMaxBirthProb() * (1 - popDensity)
        if random.random() < birthProb:
            offspring = SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
            return offspring
        else:
            raise NoChildException
        


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses[:]

    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.getViruses())     

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        for virus in self.getViruses():
            if virus.doesClear():
                self.viruses.remove(virus)

        popDensity = self.getTotalPop() / self.getMaxPop()

        for virus in self.getViruses():
            try:
                self.viruses.append(virus.reproduce(popDensity))
            except NoChildException:
                pass
        
        return self.getTotalPop()



#
# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb, numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    timeSteps = 3000

    # For each time step its average population over number of trials
    sums_of_populations = [0 for i in range(timeSteps)]
    for trial in range(numTrials):
        viruses = [SimpleVirus(maxBirthProb, clearProb) for i in range(numViruses)]
        patient = Patient(viruses, maxPop)
        for timeStep in range(timeSteps):
            sums_of_populations[timeStep] += patient.update()
    popAverage = [popSum / numTrials for popSum in sums_of_populations]
   
    # Plotting
    pylab.figure('Average population on different times')
    pylab.plot([i for i in range(timeSteps)], popAverage, label='average population')
    pylab.title('Average population on different times')
    pylab.xlabel('time')
    pylab.ylabel('population')
    pylab.xlim(0, timeSteps-1)
    pylab.ylim(0, maxPop)
    pylab.show()


    
#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.getResistances().get(drug, False)
          
    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException 
            
        birthProb = self.getMaxBirthProb() * (1 - popDensity)
        if random.random() > birthProb:
            raise NoChildException
        
        childResistances = self.getResistances().copy()
        for resistance in childResistances:
            if random.random() < self.getMutProb():
                childResistances[resistance] = not childResistances[resistance]

        return ResistantVirus(self.getMaxBirthProb(), self.getClearProb(), childResistances, self.getMutProb())
              


class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.prescriptions = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.getPrescriptions():
            self.prescriptions.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.prescriptions[:]

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        resistPop = 0
        for virus in self.getViruses():
            resistPop += 1
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    resistPop -= 1
                    break
        return resistPop
             
    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        
        # Remove some viruses
        for virus in self.getViruses()[:]:
            if virus.doesClear():
                self.viruses.remove(virus)

        # Population density
        popDensity = len(self.getViruses()) / self.getMaxPop()

        # Reproduce
        for virus in self.getViruses()[:]:
            try:
                offspring = virus.reproduce(popDensity, self.getPrescriptions())
                self.viruses.append(offspring)
            except NoChildException:
                pass
        
        return self.getTotalPop()



#
# PROBLEM 4
#
def simulationWithDrug(startPop, maxPop, maxBirthProb, clearProb, drugs, mutProb, timelyPrescriptions={}, numTrials=10, timeSteps=100):
    

    ###### Compute curves for average total population and average virus resistant population
    
    total_pop_sums = [0 for i in range(timeSteps)]
    resist_pop_sums = [0 for i in range(timeSteps)]

    # Run the trials and generate information about total and resistant population over time for each trial
    for trial in range(numTrials):
        resistances = {drug : False for drug in drugs}
        viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for i in range(startPop)]
        patient = TreatedPatient(viruses, maxPop)

        for timeStep in range(timeSteps):
            # Add a drug if its time for it
            if timeStep in timelyPrescriptions:
                patient.addPrescription(timelyPrescriptions[timeStep])

            total_pop_sums[timeStep] += patient.update()
            resist_pop_sums[timeStep] += patient.getResistPop(patient.getPrescriptions())

    # Get averages from sums
    total_pop_averages = [i / numTrials for i in total_pop_sums]
    resist_pop_averages = [i / numTrials for i in resist_pop_sums]


    ###### Plot the curves
    pylab.figure('Medicated Simulation')
    pylab.title('Medicated Simulation')
    pylab.plot([i for i in range(timeSteps)], total_pop_averages, label = 'All viruses', color='grey')
    pylab.plot([i for i in range(timeSteps)], resist_pop_averages, label = 'Drug-resistant viruses', color='yellow')
    pylab.axhline(y=maxPop, label='Max possible population', color='black')
    for timeStep in timelyPrescriptions:
        pylab.axvline(x=timeStep,  label=f'"{timelyPrescriptions[timeStep]}" prescribed')
    pylab.xlabel('Time steps')
    pylab.ylabel('Average population')
    pylab.legend()
    pylab.show()

    

