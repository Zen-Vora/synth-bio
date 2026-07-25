import unittest

from connection import Connection
from neuron import Neuron


class PlasticityTests(unittest.TestCase):
    def test_connection_strengthens_when_target_fires_shortly_after_source(self):
        source = Neuron(unique_id=0)
        target = Neuron(unique_id=1)
        connection = Connection(
            unique_id=2,
            source_neuron=source,
            target_neuron=target,
            weight=0.50,
        )

        connection.record_source_fire(3)
        connection.apply_stdp(current_tick=4)

        self.assertGreater(connection.weight, 0.50)

    def test_connection_weakens_when_target_fires_late(self):
        source = Neuron(unique_id=0)
        target = Neuron(unique_id=1)
        connection = Connection(
            unique_id=2,
            source_neuron=source,
            target_neuron=target,
            weight=0.50,
        )

        connection.record_source_fire(1)
        connection.apply_stdp(current_tick=6)

        self.assertLess(connection.weight, 0.50)

    def test_neuron_rewards_contributors_when_activation_is_near_threshold(self):
        source = Neuron(unique_id=0)
        target = Neuron(unique_id=1)
        connection = Connection(
            unique_id=2,
            source_neuron=source,
            target_neuron=target,
            weight=0.50,
        )
        target.fire_threshold = 1.0

        target.receive(0.8, connection)
        target.update(current_tick=3)

        self.assertGreater(connection.weight, 0.50)

    def test_neuron_rewards_all_contributors_when_it_fires(self):
        source_a = Neuron(unique_id=0)
        source_b = Neuron(unique_id=1)
        target = Neuron(unique_id=2)
        connection_a = Connection(
            unique_id=3,
            source_neuron=source_a,
            target_neuron=target,
            weight=0.50,
        )
        connection_b = Connection(
            unique_id=4,
            source_neuron=source_b,
            target_neuron=target,
            weight=0.50,
        )
        target.fire_threshold = 0.8

        target.receive(0.3, connection_a)
        target.receive(0.5, connection_b)
        target.update(current_tick=4)

        self.assertGreater(connection_a.weight, 0.50)
        self.assertGreater(connection_b.weight, 0.50)


if __name__ == "__main__":
    unittest.main()
