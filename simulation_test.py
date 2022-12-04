import pytest
from simulation import Simulation

def test_create_population():

    assert len(sim.population) == sim.pop_size

    for i in sim.initial_infected_i:
        assert sim.population[i].infected == True

def test_interaction():

    len(sim.interaction(100))

def test_infect_newly_infected():

    sim1 = Simulation("oogabooga", 10000, 0, initial_infected=0) #used 0 initial infections because the check for current infection is in interaction() method 

    sim1._infect_newly_infected(sim1.population)

    assert len(sim1.infected) == 10000


sim = Simulation("oogabooga", 10000, 0)