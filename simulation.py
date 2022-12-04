import random, sys
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


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

        self.initial_infected_i = (random.choices(range(1, self.pop_size), k=initial_infected))
        self.infected = []

        for infected in self.initial_infected_i:
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
        if self.pop_size < 0 or self.vacc_percentage >= 1: #TODO add vaccination check
            return False
        return True


    def run(self):
        # This method starts the simulation. It should track the number of 
        # steps the simulation has run and check if the simulation should 
        # continue at the end of each step. 

        time_step_counter = 0
        should_continue = True

        # TODO: Write meta data to the logger. This should be starting 
        # statistics for the simulation. It should include the initial
        # population size and the virus. 
        self.logger.write_metadata(self.pop_size, self.virus)
        self.step_number = 0

        while should_continue:
            # TODO: Increment the time_step_counter
            # TODO: for every iteration of this loop, call self.time_step() 
            # Call the _simulation_should_continue method to determine if 
            # the simulation should continue
            time_step_counter += 1
            should_continue = self.time_step()
            self.step_number += 1

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
        num_infected = len(self.infected)
        for i in range(num_infected):
            new_interactions = self.interaction(100)
            new_infections = self._infect_newly_infected(new_interactions)
            
            for new_infection in new_infections:
                if self._simulation_should_continue():
                    if self.infected[i].did_survive_infection():
                        self.vacc_percentage += 1/self.original_pop_size
                        new_survivors += 1
                    else:
                        self.pop_size -= 1
                        new_deaths += 1
                else:
                    return False

            self.logger.log_interactions(self.step_number, self.pop_size, len(new_interactions))
            self.logger.log_infections(self.step_number, self.pop_size, len(new_infections))
            self.logger.log_infection_survival(self.step_number, self.pop_size, new_deaths)

            return True

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

        interacted_with = random.choices(self.population, k=100)

        return interacted_with

    def _infect_newly_infected(self, interacted_with):
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        newly_infected = []

        vaccinated_population = []

        infectable = []

        for person in interacted_with:
            if not person.is_vaccinated:
                infectable.append(person)

        for people in infectable:
            if random.random() > virus.repro_rate:
                newly_infected.append(people)
        
        for infected in newly_infected:
            self.population[infected.id].infection = virus
            self.infected.append(infected)

        return newly_infected


if __name__ == "__main__":
    # Test your simulation here
    virus_name = "Sniffles"
    repro_num = 0.5
    mortality_rate = 0.12
    virus = Virus(virus_name, repro_num, mortality_rate)

    # Set some values used by the simulation
    pop_size = 1000
    vacc_percentage = 0.1
    initial_infected = 10

    # Make a new instance of the simulation
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    # sim.run()
    sim.run()
