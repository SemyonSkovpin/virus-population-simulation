from ps3b import *



def simulationWithDrugV2(startPop, maxPop, maxBirthProb, clearProb, drugs, mutProb, timelyPrescriptions={}, numTrials=10, timeSteps=100):
    '''
    Run the simulation with TreatedPatient, ResistantVirus instances, on parameters given above. Plot the data from the simulation.

    :timelyPrescriptions: {timeStep : list(str drugs to add)}
    '''

    # Run it for a number of trials to then compute averages among the trials.
    # Save data curves among different trials.
    total_pop_curves = []
    resistant_pop_curves = []

    for trial in range(numTrials):
        # Initiate TreatedPatient and some ResistantViruses for current trial
        resistances = {drug : False for drug in drugs}
        viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for i in range(startPop)]
        patient = TreatedPatient(viruses, maxPop)

        # Log this trial's data curves 
        total_pop_curves.append([])
        resistant_pop_curves.append([])
        

        # Run the simulation through timesteps
        for timeStep in range(timeSteps):
            '''
            # delete all unresistant viruses
            if timeStep == 300:
                for virus in patient.getViruses():
                    for drug in patient.getPrescriptions():
                        if not virus.isResistantTo(drug):
                            patient.viruses.remove(virus)
                            break
            '''

            # Add active drugs to simulation if they are scheduled on this timestep
            if timeStep in timelyPrescriptions:
                for drug in timelyPrescriptions[timeStep]:
                    patient.addPrescription(drug)

            # Update the simulation
            # Record the total and resistant population for each timestep
            total_population = patient.update()
            resistant_population = patient.getResistPop(patient.getPrescriptions())
            total_pop_curves[-1].append(total_population)
            resistant_pop_curves[-1].append(resistant_population)

    # For each timestep calculate its average population among trials
    def get_avg_curve(pop_curves):
        average_curve = []
        for timeStep in range(timeSteps):
            average_curve.append(sum([population_curve[timeStep] for population_curve in pop_curves]) / numTrials)
        return average_curve

    avg_total_pop = get_avg_curve(total_pop_curves)
    avg_resist_pop = get_avg_curve(resistant_pop_curves)

    # Make the plot for this simulation
    pylab.figure('Virus population simulation')
    pylab.xlabel('Time steps')
    pylab.ylabel('Average populaton')

    pylab.plot(avg_total_pop, label='All viruses')
    pylab.plot(avg_resist_pop, label='Drug-resistant viruses')

    # Separating lines that indicate introduction of certain drugs
    for timeStep in timelyPrescriptions:
        addedDrugs = [drug for drug in timelyPrescriptions[timeStep]]
        pylab.axvline(x=timeStep, label=f'Prescribed drugs: {", ".join(addedDrugs)}', color='red')

    #'''
    # Show population limit
    pylab.axhline(y=maxPop, label='Maximum population', color='black')
    #'''

    pylab.legend()
    pylab.show()



# Simulation parameters
params = {
    'startPop'     : 10,
    'maxPop'       : 1000,
    'maxBirthProb' : 0.1,
    'clearProb'    : 0.05,
    'mutProb'      : 0.0,
    'drugs'        : ['A', 'B', 'C', 'D', 'E'],
    'timelyPrescriptions' : {},

    'numTrials'      : 1,
    'timeSteps'      : 500
}

# Run simulation and make plot
simulationWithDrugV2(**params)


