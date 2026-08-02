import os
import tempfile
import unittest

from brain import Brain
from neuron import Neuron
from main import build_scaffold_connections


class SelfOrganizationTests(unittest.TestCase):
    def test_inhibitory_neuron_uses_different_params(self):
        neuron = Neuron(unique_id=0, neuron_type="INHIBITORY")

        self.assertGreater(neuron.fire_threshold, 1.0)
        self.assertGreater(neuron.refractory_period, 1)
        self.assertLess(neuron.decay_rate, 0.1)

    def test_brain_can_create_new_connection_when_requested(self):
        brain = Brain()
        source = brain.create_neuron(neuron_type="EXCITATORY")
        target = brain.create_neuron(neuron_type="MEMORY")

        created = brain.grow_connection(source, target, weight=0.05)

        self.assertTrue(created)
        self.assertEqual(len(brain.connections), 1)

    def test_brain_can_prune_weak_inactive_connection(self):
        brain = Brain()
        source = brain.create_neuron(neuron_type="EXCITATORY")
        target = brain.create_neuron(neuron_type="MEMORY")
        connection = brain.grow_connection(source, target, weight=0.01)
        connection.last_activity_tick = 0

        pruned = brain.prune_connection(connection, current_tick=50)

        self.assertTrue(pruned)
        self.assertEqual(len(brain.connections), 0)

    def test_scaffold_connects_each_neuron_to_five_neighbors(self):
        brain = Brain()
        neurons = [brain.create_neuron() for _ in range(6)]

        build_scaffold_connections(brain, neurons)

        for neuron in neurons:
            self.assertGreaterEqual(len(neuron.outgoing_connections), 5)

    def test_brain_can_persist_and_resume_state(self):
        brain = Brain()
        brain.chemistry["serotonin"] = 0.9
        brain.motivation["curiosity"] = 0.8
        brain.world.body_energy = 88.0
        path = tempfile.NamedTemporaryFile(delete=False, suffix=".pkl").name
        try:
            brain.save(path)
            loaded = Brain.load(path)

            self.assertEqual(loaded.chemistry["serotonin"], 0.9)
            self.assertEqual(loaded.motivation["curiosity"], 0.8)
            self.assertEqual(loaded.world.body_energy, 88.0)
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_adapt_structure_can_grow_new_neuron_when_conditions_are_favorable(self):
        brain = Brain()
        for _ in range(3):
            brain.create_neuron()

        brain.chemistry["acetylcholine"] = 0.9
        brain.chemistry["dopamine"] = 0.8
        brain.motivation["curiosity"] = 0.9
        brain.motivation["reward_expectation"] = 0.9
        for neuron in brain.neurons:
            neuron.fire_count = 5

        before = len(brain.neurons)
        brain.adapt_structure()

        self.assertGreater(len(brain.neurons), before)

    def test_output_neurons_can_collectively_choose_action(self):
        brain = Brain()
        left = brain.create_neuron(neuron_type="OUTPUT")
        right = brain.create_neuron(neuron_type="OUTPUT")
        left.action_preferences = {"move_left": 0.8, "eat": 0.2}
        right.action_preferences = {"move_left": 0.2, "eat": 0.8}
        brain.motivation["energy"] = 0.1

        chosen = brain.choose_action_from_output_neurons([left, right])

        self.assertEqual(chosen, "eat")
