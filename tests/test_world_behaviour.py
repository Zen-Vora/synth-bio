import unittest

from neuron import Neuron
from world import World


class WorldBehaviourTests(unittest.TestCase):
    def test_eat_action_reduces_food_and_increases_reward(self):
        world = World(food=4.0, reward=0.0, body_energy=10.0)

        world.apply_action("eat")

        self.assertLess(world.food, 4.0)
        self.assertGreater(world.reward, 0.0)
        self.assertGreater(world.body_energy, 10.0)

    def test_neuron_cannot_fire_when_energy_is_too_low(self):
        neuron = Neuron(unique_id=0, fire_threshold=0.1)
        neuron.energy = 5.0
        neuron.energy_fire_threshold = 6.0

        neuron.receive(1.0)
        fired = neuron.update(current_tick=1)

        self.assertFalse(fired)
