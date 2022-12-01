import pytest
from simulation import Simulation

def test_create_population():

    assert len(sim.population) == sim.pop_size
    
    for i in sim.initial_infected_i:
        assert sim.population[i].infected == True

def test_interaction():

    len(sim.interaction(100))

sim = Simulation("oogabooga", 1000, 0)