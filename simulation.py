import random, sys
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus
import argparse


class Simulation(object):
    def __init__(self, pop_size, vacc_percentage, initial_infected, virus):
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        self.logger = Logger(virus.name + ".txt")
        # TODO: Store the virus in an attribute
        self.virus = virus
        # TODO: Store pop_size in an attribute
        self.original_pop_size = pop_size
        self.pop_size = pop_size
        # TODO: Store the vacc_percentage in a variable
        self.vacc_percentage = vacc_percentage
        self.vaccinated = []
        # TODO: Store initial_infected in a variable
        self.initial_infected = initial_infected
        #to speed up looking for infected persons they are all stored here
        self.infected = []
        # You need to store a list of people (Person instances)
        # Some of these people will be infected some will not. 
        # Use the _create_population() method to create the list and 
        # return it storing it in an attribute here. 
        # TODO: Call self._create_population() and pass in the correct parameters.
        self.population = self._create_population(initial_infected)

    def _create_population(self, initial_infected):
        # TODO: Create a list of people (Person instances). This list 
        # should have a total number of people equal to the pop_size. 
        # Some of these people will be uninfected and some will be infected.
        # The number of infected people should be equal to the the initial_infected
        # TODO: Return the list of people

        population = []

        for i in range(self.pop_size):
            population.append(Person(i))

        vaccinated_i = (random.choices(range(1, self.pop_size), k=int(self.vacc_percentage*self.pop_size//1)))
        self.vaccinated = []

        for vaccinated in vaccinated_i:
            population[vaccinated] = (Person(vaccinated, is_vaccinated=False, infection=self.virus))
            self.vaccinated.append(population[vaccinated])

        initial_infected_i = (random.choices(range(1, self.pop_size), k=initial_infected))
        self.infected = []

        for infected in initial_infected_i:
            population[infected] = (Person(infected, is_vaccinated=False, infection=self.virus))
            self.infected.append(population[infected])

        return population


    def _simulation_should_continue(self):
        # This method will return a boolean indicating if the simulation 
        # should continue. 
        # The simulation should not continue if all of the people are dead, 
        # or if all of the living people have been vaccinated. 
        # TODO: Loop over the list of people in the population. Return True
        # if the simulation should continue or False if not.
        if self.pop_size <= 0 or len(self.vaccinated) >= self.pop_size:
            return False
        return True


    def run(self):
        # This method starts the simulation. It should track the number of 
        # steps the simulation has run and check if the simulation should 
        # continue at the end of each step. 

        should_continue = True

        # TODO: Write meta data to the logger. This should be starting 
        # statistics for the simulation. It should include the initial
        # population size and the virus. 
        self.step_number = 0


        self.logger.write_metadata(self.pop_size, self.virus, self.initial_infected)

        while should_continue:
            # TODO: Increment the time_step_counter
            # TODO: for every iteration of this loop, call self.time_step() 
            # Call the _simulation_should_continue method to determine if 
            # the simulation should continue
            
            
            self.time_step()
            should_continue = self._simulation_should_continue()

        self.logger.log_time_step(self.step_number, self.pop_size)
        
        # TODO: When the simulation completes you should conßclude this with 
        # the logger. Send the final data to the logger. 
        
    def time_step(self):
        # This method will simulate interactions between people, calulate 
        # new infections, and determine if vaccinations and fatalities from infections
        # The goal here is have each infected person interact with a number of other 
        # people in the population
        # TODO: Loop over your population
        # For each person if that person is infected
        # have that person interact with 100 other living people 
        # Run interactions by calling the interaction method below. That method
        # takes the infected person and a random person

        new_deaths = 0
        new_survivors = 0
        number_of_new_interactions = 0
        number_of_new_infections = 0
        current_infected = []
        for person in self.infected:
            if person.is_alive:
                current_infected.append(person)

        for infected in current_infected:
                
            new_interactions = self.interaction(100)
            new_infections = self._infect_newly_infected(new_interactions)

            if infected.did_survive_infection():
                infected.is_vaccinated = True   #since surviving a virus gives similar results to vaccine
                self.vaccinated.append(infected)
                new_survivors += 1
            else:
                infected.is_alive = False
                self.pop_size -= 1
                new_deaths += 1

        
        self.step_number += 1

        self.logger.log_interactions(self.step_number, self.pop_size, number_of_new_interactions)
        self.logger.log_infections(self.step_number, self.pop_size, number_of_new_infections)
        self.logger.log_infection_survival(self.step_number, self.pop_size, new_deaths)

    def interaction(self, num_interactions):
        # TODO: Finish this method.
        # The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0.0 and 1.0.  If that number is smaller
            #     than repro_rate, add that person to the newly infected array
            #     Simulation object's newly_infected array, so that their infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call logger method during this method.

        infectable = list(set(self.population).difference(set(self.infected).union(set(self.vaccinated))))

        if len(infectable) >= 100:
            interacted_with = random.choices(infectable, k=100)
        else:
            interacted_with = random.choices(infectable, k=len(infectable))

        return interacted_with

    def _infect_newly_infected(self, interacted_with):
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        newly_infected = []

        for infected in interacted_with:
            if random.random() < self.virus.repro_rate and infected.infection == None:
                newly_infected.append(infected)
                self.population[infected.id].infection = self.virus
                self.infected.append(infected)

        return newly_infected


if __name__ == "__main__":
    # # Test your simulation here
    # virus_name = "Sniffles"
    # repro_num = 0.5
    # mortality_rate = 0.12
    # virus = Virus(virus_name, repro_num, mortality_rate)

    # # Set some values used by the simulation
    # pop_size = 1000
    # vacc_percentage = 0.1
    # initial_infected = 10

    # # Make a new instance of the simulation
    # sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    parser = argparse.ArgumentParser()
    parser.add_argument("population_size", help="size of the population you wish to simulate", type=int)
    parser.add_argument("vacc_percentage", help="percent of people who start vaccinated within given population", type=float)
    parser.add_argument("virus", help="name of the virus")
    parser.add_argument("mortality_rate", help="the percent chance of dying after contracting the virus", type=float)
    parser.add_argument("reproduction_rate", help="the percent chance of transmission per interaction", type=float)
    parser.add_argument("initial_infected", help="the number of people who start with the virus", type=int)

    args = parser.parse_args()
    virus = Virus(args.virus, repro_rate=args.reproduction_rate, mortality_rate=args.mortality_rate)
    sim = Simulation(args.population_size, args.vacc_percentage, args.initial_infected, virus)
    # sim.run()
    sim.run()
