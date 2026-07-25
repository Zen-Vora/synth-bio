# Brain module for the SynthBio simulation.
#
# This module defines the Brain class, which keeps a list of neurons and
# connections, advances simulation time, delivers signals, and coordinates
# neuron updates.

from neuron import Neuron, STATE_RESTING, DEFAULT_NEURON_TYPE
from connection import Connection


class Brain:
    # Brain is a simple container for neurons and connections.
    # It advances time and coordinates signal delivery.
    def __init__(
        self,
        neurons=None,
        connections=None,
        current_tick=0,
        next_available_id=0,
    ):
        # List of all neurons in the brain.
        self.neurons = [] if neurons is None else neurons
        # List of all connections in the brain.
        self.connections = [] if connections is None else connections
        # Simulation tick counter.
        self.current_tick = current_tick
        # Next ID to assign for newly created neurons/connections.
        self.next_available_id = next_available_id
        # Record the firing paths produced in the last tick.
        self.last_firing_paths = []

    def create_neuron(
        self,
        current_activation=0.0,
        fire_threshold=1.0,
        max_activation=1.0,
        current_state=STATE_RESTING,
        refractory_timer=0,
        input_buffer=None,
        output_strength=0.0,
        incoming_connections=None,
        outgoing_connections=None,
        last_fire_tick=None,
        age=0,
        neuron_type=DEFAULT_NEURON_TYPE,
    ):
        # Create a neuron and assign a unique ID automatically.
        neuron = Neuron(
            unique_id=self.next_available_id,
            current_activation=current_activation,
            fire_threshold=fire_threshold,
            max_activation=max_activation,
            current_state=current_state,
            refractory_timer=refractory_timer,
            input_buffer=input_buffer,
            output_strength=output_strength,
            incoming_connections=incoming_connections,
            outgoing_connections=outgoing_connections,
            last_fire_tick=last_fire_tick,
            age=age,
            neuron_type=neuron_type,
        )
        # Add the new neuron to the brain.
        self.neurons.append(neuron)
        # Reserve the next unique ID for the following new object.
        self.next_available_id += 1
        return neuron

    def create_connection(
        self,
        source_neuron,
        target_neuron,
        weight=1.0,
        signal_delay=0,
        enabled=True,
    ):
        # Create a connection and assign a unique ID automatically.
        connection = Connection(
            unique_id=self.next_available_id,
            source_neuron=source_neuron,
            target_neuron=target_neuron,
            weight=weight,
            signal_delay=signal_delay,
            enabled=enabled,
        )
        # Wire the connection into both neurons.
        source_neuron.outgoing_connections.append(connection)
        target_neuron.incoming_connections.append(connection)
        # Add the connection to the brain's list.
        self.connections.append(connection)
        # Reserve the next unique ID for the following new object.
        self.next_available_id += 1
        return connection

    def tick(self):
        # Advance the global simulation tick counter.
        self.current_tick += 1

        # Deliver signals from connections to target neurons.
        for connection in self.connections:
            delivered_signal = connection.advance()
            if delivered_signal is None:
                continue
            connection.target_neuron.receive(delivered_signal, connection)

        # Ask every neuron to update itself.
        firing_neurons = []
        self.last_firing_paths = []
        for neuron in self.neurons:
            if neuron.update(self.current_tick):
                firing_neurons.append(neuron)

        # Record source firing times and let plastic synapses adapt.
        for neuron in firing_neurons:
            for connection in neuron.outgoing_connections:
                connection.record_source_fire(self.current_tick)

        for neuron in firing_neurons:
            for connection in neuron.incoming_connections:
                connection.apply_stdp(self.current_tick)

        # After neurons decide to fire, let the brain dispatch outgoing signals.
        for neuron in firing_neurons:
            for connection in neuron.outgoing_connections:
                connection.transmit(neuron.output_strength)
                self.last_firing_paths.append((neuron, connection.target_neuron))

    def visualize(self):
        # Print a simple text graph for the most recent firing paths.
        if not self.last_firing_paths:
            print("No firing paths to visualize this tick.")
            return

        for source, target in self.last_firing_paths:
            print(f"Neuron {source.unique_id}")
            print(" |")
            print(" | fires")
            print(" v")
            print(f"Neuron {target.unique_id}")
            print()

    def inspect_network(self):
        # Print the current network connection structure.
        print("=== Network structure ===")
        for neuron in self.neurons:
            print(f"\nNeuron {neuron.unique_id} ({neuron.neuron_type})")
            if not neuron.outgoing_connections:
                print("  (no outgoing connections)")
                continue
            for connection in neuron.outgoing_connections:
                target_id = connection.target_neuron.unique_id
                print(
                    f"  → Neuron {target_id} (weight: {connection.weight:.2f}, "
                    f"delay: {connection.signal_delay}, enabled: {connection.enabled})"
                )
        print("=== End network structure ===")

    def collect_stats(self):
        # Collect a small summary of the current network state.
        firing_neurons = [neuron for neuron in self.neurons if neuron.current_state == "REFRACTORY"]
        average_weight = 0.0
        if self.connections:
            average_weight = sum(connection.weight for connection in self.connections) / len(self.connections)

        if self.connections:
            strongest_connection = max(self.connections, key=lambda connection: connection.weight)
            weakest_connection = min(self.connections, key=lambda connection: connection.weight)
        else:
            strongest_connection = None
            weakest_connection = None

        average_activation = 0.0
        if self.neurons:
            average_activation = sum(neuron.current_activation for neuron in self.neurons) / len(self.neurons)

        return {
            "firing_neurons": len(firing_neurons),
            "average_connection_weight": average_weight,
            "strongest_connection": strongest_connection,
            "weakest_connection": weakest_connection,
            "average_activation": average_activation,
        }

    def print_stats(self):
        # Print a compact summary of the current network state.
        stats = self.collect_stats()
        print(f"Tick {self.current_tick}")
        print(f"Firing neurons: {stats['firing_neurons']}")
        print(f"Average connection weight: {stats['average_connection_weight']:.2f}")
        if stats["strongest_connection"] is not None:
            print(
                "Strongest connection: "
                f"{stats['strongest_connection'].source_neuron.unique_id} → "
                f"{stats['strongest_connection'].target_neuron.unique_id} "
                f"({stats['strongest_connection'].weight:.2f})"
            )
        if stats["weakest_connection"] is not None:
            print(
                "Weakest connection: "
                f"{stats['weakest_connection'].source_neuron.unique_id} → "
                f"{stats['weakest_connection'].target_neuron.unique_id} "
                f"({stats['weakest_connection'].weight:.2f})"
            )
        print(f"Average activation: {stats['average_activation']:.2f}")
