import pytest
from simulation import Simulation

def test_create_population():
    sim = Simulation("oogabooga", 50, 0)

    assert len(sim.population) == sim.pop_size
    
    for i in sim.initial_infected_i:
        assert sim.population[i].infected == True

def test_interaction():
    sim = Simulation("oogabooga", 1000, 0)

    len(sim.interaction(100))