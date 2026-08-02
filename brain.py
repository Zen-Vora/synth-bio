# Brain module for the SynthBio simulation.
#
# This module defines the Brain class, which keeps a list of neurons and
# connections, advances simulation time, delivers signals, and coordinates
# neuron updates.

import os
import pickle

from neuron import Neuron, STATE_RESTING, DEFAULT_NEURON_TYPE
from connection import Connection
from world import World


class Brain:
    # Brain is a simple container for neurons and connections.
    # It advances time and coordinates signal delivery.
    def __init__(
        self,
        neurons=None,
        connections=None,
        current_tick=0,
        next_available_id=0,
        world=None,
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
        # Actions produced by output neurons during the last tick.
        self.last_actions = []
        # Environment that can respond to output actions.
        self.world = world if world is not None else World()
        # Sensory neurons that receive signals from the world each tick.
        self.sensory_neurons = []
        # Neuromodulators that bias behavior globally.
        self.chemistry = {
            "dopamine": 0.6,
            "serotonin": 0.6,
            "acetylcholine": 0.6,
            "noradrenaline": 0.55,
        }
        # Internal motivation state.
        self.motivation = {
            "curiosity": 0.7,
            "energy": 0.6,
            "stress": 0.2,
            "reward_expectation": 0.5,
        }
        self.structural_changes = {"added": 0, "removed": 0, "strengthened": 0, "weakened": 0}
        self.last_report_tick = 0
        self.last_report_structural_changes = dict(self.structural_changes)

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
        excitatory=True,
        synaptic_fatigue=1.0,
        homeostasis_target=0.0,
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
            excitatory=excitatory,
            synaptic_fatigue=synaptic_fatigue,
            homeostasis_target=homeostasis_target,
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

    def register_sensor(self, neuron, sensor_name):
        # Register a neuron as a sensory neuron for one property in the world.
        self.sensory_neurons.append((neuron, sensor_name))

    def tick(self):
        # Advance the global simulation tick counter.
        self.current_tick += 1

        # Let the world change a little each tick.
        self.world.tick()

        # Feed the current world state into any registered sensory neurons.
        for neuron, sensor_name in self.sensory_neurons:
            neuron.receive(self.world.get_sensor_signal(sensor_name))

        # Deliver signals from connections to target neurons.
        for connection in self.connections:
            delivered_signals = connection.advance(self.current_tick)
            for delivered_signal in delivered_signals:
                connection.target_neuron.receive(delivered_signal, connection)

        # Ask every neuron to update itself.
        firing_neurons = []
        self.last_firing_paths = []
        self.last_actions = []
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
                connection.transmit(neuron.output_strength, self.current_tick)
                self.last_firing_paths.append((neuron, connection.target_neuron))

        # Output neurons can act on the environment based on their own preferences.
        output_neurons = [neuron for neuron in firing_neurons if neuron.neuron_type == "OUTPUT"]
        if output_neurons:
            selected_action = self.choose_action_from_output_neurons(output_neurons)
            if selected_action:
                self.world.apply_action(selected_action)
                self.last_actions.append(selected_action)

        # Update motivations from recent activity and environment.
        self.update_motivations(firing_neurons)

        # Apply neuromodulator-driven behavior changes and structural plasticity.
        self.apply_neuromodulation()
        self.adapt_structure()

        if self.current_tick % 25 == 0:
            self.print_brain_report()

    def grow_connection(self, source_neuron, target_neuron, weight=0.05, signal_delay=0, enabled=True):
        # Create a new connection when the topology should expand.
        if source_neuron is target_neuron:
            return None
        if any(connection.source_neuron is source_neuron and connection.target_neuron is target_neuron for connection in self.connections):
            return None
        connection = self.create_connection(source_neuron, target_neuron, weight=weight, signal_delay=signal_delay, enabled=enabled)
        self.structural_changes["added"] += 1
        return connection

    def prune_connection(self, connection, current_tick):
        # Drop only truly weak or stale connections so the initial scaffold remains intact.
        if connection is None:
            return False
        if connection.weight <= 0.04:
            self.remove_connection(connection)
            self.structural_changes["removed"] += 1
            return True
        if (
            connection.last_source_fire_tick is not None
            and (current_tick - connection.last_source_fire_tick) > 50
            and connection.weight <= 0.20
        ):
            self.remove_connection(connection)
            self.structural_changes["removed"] += 1
            return True
        return False

    def remove_connection(self, connection):
        if connection is None:
            return False
        connection.source_neuron.outgoing_connections = [c for c in connection.source_neuron.outgoing_connections if c is not connection]
        connection.target_neuron.incoming_connections = [c for c in connection.target_neuron.incoming_connections if c is not connection]
        self.connections = [c for c in self.connections if c is not connection]
        return True

    def apply_neuromodulation(self):
        # Modulate plasticity and firing tendencies globally.
        dopamine = self.chemistry["dopamine"]
        serotonin = self.chemistry["serotonin"]
        acetylcholine = self.chemistry["acetylcholine"]
        noradrenaline = self.chemistry["noradrenaline"]

        for neuron in self.neurons:
            neuron.adapt_to_context(self.chemistry, self.motivation)
            neuron.fire_threshold = max(0.4, neuron.fire_threshold + 0.001 * (noradrenaline - 0.5))
            neuron.synaptic_fatigue = max(0.2, neuron.synaptic_fatigue - 0.001 * (dopamine - 0.5))
            neuron.plasticity_rate = max(0.01, neuron.plasticity_rate + 0.001 * (acetylcholine - 0.5))

        self.chemistry["dopamine"] = min(1.0, max(0.0, self.chemistry["dopamine"] + 0.01 * (self.motivation["reward_expectation"] - 0.5) + 0.004 * (self.world.reward - 0.5)))
        self.chemistry["serotonin"] = min(1.0, max(0.0, self.chemistry["serotonin"] + 0.01 * (self.motivation["energy"] - 0.5) + 0.003 * (1.0 - self.world.danger)))
        self.chemistry["acetylcholine"] = min(1.0, max(0.0, self.chemistry["acetylcholine"] + 0.01 * (self.motivation["curiosity"] - 0.5) + 0.002 * self.world.noise))
        self.chemistry["noradrenaline"] = min(1.0, max(0.0, self.chemistry["noradrenaline"] + 0.01 * (self.motivation["stress"] - 0.2) + 0.003 * self.world.danger))

    def update_motivations(self, firing_neurons):
        # Drive motivation states from environment, action success, and recent activity.
        recent_activity = sum(neuron.fire_count for neuron in self.neurons)
        reward_signal = self.world.reward
        energy_signal = max(0.0, min(1.0, self.world.body_energy / 100.0))
        stress_signal = max(0.0, min(1.0, self.world.danger + 0.2 * (1.0 - energy_signal)))

        self.motivation["curiosity"] = min(1.0, max(0.0, self.motivation["curiosity"] + 0.01 * (self.chemistry["acetylcholine"] - 0.5) + 0.005 * (reward_signal - 0.5)))
        self.motivation["energy"] = min(1.0, max(0.0, self.motivation["energy"] + 0.01 * (energy_signal - 0.5) - 0.003 * (recent_activity / max(1, len(self.neurons)))))
        self.motivation["stress"] = min(1.0, max(0.0, self.motivation["stress"] + 0.008 * (stress_signal - 0.5) + 0.003 * (1.0 - energy_signal)))
        self.motivation["reward_expectation"] = min(1.0, max(0.0, self.motivation["reward_expectation"] + 0.008 * (reward_signal - 0.3) + 0.004 * (self.chemistry["dopamine"] - 0.5)))

    def adapt_structure(self):
        # Grow new neurons when the network is active and the chemistry is favorable.
        if (
            self.current_tick % 6 == 0
            and self.motivation["curiosity"] > 0.4
            and self.chemistry["acetylcholine"] > 0.4
            and self.chemistry["dopamine"] > 0.35
        ):
            candidate = self.create_neuron(
                output_strength=0.55,
                fire_threshold=0.8,
                neuron_type="NORMAL",
                excitatory=True,
            )
            self.structural_changes["added"] += 1
            if len(self.neurons) > 1:
                for source in self.neurons[-3:]:
                    if source is candidate:
                        continue
                    self.grow_connection(source, candidate, weight=0.12)
                    self.grow_connection(candidate, source, weight=0.10)

        # Grow or prune connections based on recent activity and weight.
        active_neurons = [neuron for neuron in self.neurons if neuron.fire_count > 0]
        if active_neurons and self.current_tick % 5 == 0:
            for source_neuron in active_neurons[:4]:
                for target_neuron in active_neurons[1:5]:
                    if source_neuron is target_neuron:
                        continue
                    if any(connection.source_neuron is source_neuron and connection.target_neuron is target_neuron for connection in self.connections):
                        continue
                    if self.motivation["curiosity"] > 0.35 and self.chemistry["acetylcholine"] > 0.4:
                        self.grow_connection(source_neuron, target_neuron, weight=0.06)

        for connection in list(self.connections):
            last_fire_tick = getattr(connection, "last_source_fire_tick", None)
            if last_fire_tick is None:
                continue
            if self.current_tick - last_fire_tick > 20 and connection.weight <= 0.15:
                self.prune_connection(connection, self.current_tick)

    def save(self, path):
        # Persist the full brain state to disk so it can be resumed later.
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "wb") as handle:
            pickle.dump(self.__dict__, handle)

    @classmethod
    def load(cls, path):
        with open(path, "rb") as handle:
            state = pickle.load(handle)
        brain = cls()
        brain.__dict__.update(state)
        return brain

    def choose_action_from_output_neurons(self, output_neurons):
        # Let the network choose an action from a consensus of output-neuron preferences.
        if not output_neurons:
            return None

        action_scores = {}
        for neuron in output_neurons:
            preferences = getattr(neuron, "action_preferences", {})
            if not preferences:
                preferences = {
                    "move_left": 0.2,
                    "move_right": 0.2,
                    "eat": 0.2,
                    "sleep": 0.2,
                    "look": 0.1,
                    "grab": 0.1,
                }

            total_preference = sum(preferences.values())
            if total_preference <= 0.0:
                continue

            normalized_preferences = {
                action: strength / total_preference for action, strength in preferences.items()
            }
            neuron_weight = 0.6 + 0.4 * neuron.output_strength + 0.05 * min(3, neuron.fire_count)

            for action, strength in normalized_preferences.items():
                action_scores[action] = action_scores.get(action, 0.0) + strength * neuron_weight

        if not action_scores:
            return None

        # Bias the consensus toward actions that are currently useful to the brain.
        energy_need = max(0.0, 0.5 - self.motivation["energy"])
        if energy_need > 0.1:
            action_scores["eat"] = action_scores.get("eat", 0.0) + energy_need * 0.4
        if self.world.danger > 0.6:
            action_scores["move_left"] = action_scores.get("move_left", 0.0) + 0.2
            action_scores["move_right"] = action_scores.get("move_right", 0.0) + 0.2
        if self.world.reward > 0.6:
            action_scores["grab"] = action_scores.get("grab", 0.0) + 0.2

        best_action = None
        best_score = None
        for action, score in action_scores.items():
            if best_score is None or score > best_score:
                best_action = action
                best_score = score
        return best_action

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

    def print_brain_report(self):
        # Print a compact self-organization report for the brain.
        active_neurons = sorted(self.neurons, key=lambda neuron: neuron.fire_count, reverse=True)[:3]
        delta_changes = {
            name: self.structural_changes[name] - self.last_report_structural_changes.get(name, 0)
            for name in self.structural_changes
        }
        self.last_report_structural_changes = dict(self.structural_changes)
        self.last_report_tick = self.current_tick

        print("===== Brain Report =====")
        print(f"Neurons: {len(self.neurons)}")
        print(f"Connections: {len(self.connections)}")
        print("Most active neurons:")
        for neuron in active_neurons:
            print(f"  Neuron {neuron.unique_id}: fires={neuron.fire_count}, threshold={neuron.fire_threshold:.2f}")
        print("Brain chemistry:")
        for name, value in self.chemistry.items():
            print(f"  {name}: {value:.2f}")
        print("Motivations:")
        for name, value in self.motivation.items():
            print(f"  {name}: {value:.2f}")
        print("Structural changes since last report:")
        for name, value in delta_changes.items():
            print(f"  {name}: {value}")
        print("=======================")
