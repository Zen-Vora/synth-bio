# Neuron module for the SynthBio brain simulation.
#
# This module defines the Neuron class and neuron-specific constants.
# Each neuron is responsible for storing activation state, receiving
# signals, and deciding whether it should fire when updated.

# Neuron state constants.
STATE_RESTING = "RESTING"
STATE_REFRACTORY = "REFRACTORY"
# Default refractory duration used when a neuron fires.
DEFAULT_REFRACTORY_TIMER = 1

# Neuron role/type constants.
NEURON_TYPE_INPUT = "INPUT"
NEURON_TYPE_NORMAL = "NORMAL"
NEURON_TYPE_OUTPUT = "OUTPUT"
DEFAULT_NEURON_TYPE = NEURON_TYPE_NORMAL


class Neuron:
    @property
    def current_activation(self):
        return self.membrane_potential

    @current_activation.setter
    def current_activation(self, value):
        self.membrane_potential = value

    # A neuron stores the requested state fields and decides whether it fires.
    def __init__(
        self,
        unique_id,
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
        decay_rate=0.1,
        neuron_type=DEFAULT_NEURON_TYPE,
        excitatory=True,
        synaptic_fatigue=1.0,
        homeostasis_target=0.0,
    ):
        # Unique identifier for this neuron.
        self.unique_id = unique_id
        # Current membrane potential of the neuron.
        self.membrane_potential = current_activation
        # Activation threshold required to fire.
        self.fire_threshold = fire_threshold
        # Maximum activation value the neuron can hold.
        self.max_activation = max_activation
        # Current state: RESTING, REFRACTORY, or another custom label.
        self.current_state = current_state
        # Remaining refractory time before the neuron can fire again.
        self.refractory_timer = refractory_timer
        # Activation decay rate per tick.
        self.decay_rate = decay_rate
        # Cumulative count of how many times this neuron has fired.
        self.fire_count = 0
        # Incoming signals are buffered here before being integrated.
        self.input_buffer = [] if input_buffer is None else input_buffer
        # Tracks which incoming connections contributed to the most recent activation.
        self.last_activation_contributors = {}
        # Strength used for outgoing signals when this neuron fires.
        self.output_strength = output_strength
        # Connections targeting this neuron.
        self.incoming_connections = [] if incoming_connections is None else incoming_connections
        # Connections sourced from this neuron.
        self.outgoing_connections = [] if outgoing_connections is None else outgoing_connections
        # Tick index when the neuron last fired.
        self.last_fire_tick = last_fire_tick
        # Age counter for the neuron, if needed by the simulation.
        self.age = age
        # Functional role of the neuron: INPUT, NORMAL, or OUTPUT.
        self.neuron_type = neuron_type
        # Whether this neuron is excitatory (+ signal) or inhibitory (- signal).
        self.excitatory = excitatory
        # Current synaptic fatigue factor, used to reduce outgoing strength over repeated firing.
        self.synaptic_fatigue = synaptic_fatigue
        # Desired firing rate target for homeostasis.
        self.homeostasis_target = homeostasis_target
        # Track how often this neuron has fired recently for homeostatic balancing.
        self.recent_fire_count = 0
        # Energy budget available to the neuron for firing.
        self.energy = 100.0
        # Energy level below which the neuron cannot fire.
        self.energy_fire_threshold = 20.0
        # Homeostatic target firing rate.
        self.homeostasis_target = 0.2 if homeostasis_target == 0.0 else homeostasis_target

    def receive(self, signal_strength, connection=None):
        # Accept a signal and store it in the neuron's input buffer.
        self.input_buffer.append((signal_strength, connection))

    def update(self, current_tick):
        # A neuron decides whether it fires based on its own state and activation.
        # Energy is spent on firing, and the neuron regains some energy each tick.
        self.energy = min(100.0, self.energy + 0.5)

        if self.current_state == STATE_REFRACTORY:
            # Refractory neurons ignore input and count down.
            self.refractory_timer -= 1
            if self.refractory_timer <= 0:
                self.current_state = STATE_RESTING
            return False

        # Integrate all buffered input signals into activation.
        total_input = 0.0
        contributors = {}
        for entry in self.input_buffer:
            if isinstance(entry, tuple):
                signal_strength, connection = entry
            else:
                signal_strength = entry
                connection = None

            if connection is not None:
                contributors[connection] = contributors.get(connection, 0.0) + signal_strength
            total_input += signal_strength

        self.input_buffer.clear()
        adjusted_input = total_input * self.synaptic_fatigue
        if not self.excitatory:
            adjusted_input = -adjusted_input
        self.membrane_potential += adjusted_input
        self.last_activation_contributors = contributors

        # Enforce the maximum activation cap.
        if self.membrane_potential > self.max_activation:
            self.membrane_potential = self.max_activation

        # Remember the membrane state before noisy fluctuations so plasticity
        # remains predictable even when the network is lightly perturbed.
        pre_noise_membrane = self.membrane_potential

        # Add a small amount of spontaneous noise to create ongoing brain activity.
        import random

        spontaneous_noise = random.uniform(-0.005, 0.005)
        self.membrane_potential += spontaneous_noise

        # Decide whether the neuron fires this tick.
        if (
            self.membrane_potential >= self.fire_threshold
            and self.energy >= self.energy_fire_threshold
            and random.random() >= 0.01
        ):
            for connection, contribution in contributors.items():
                connection.reward_for_spike()
            self.membrane_potential = 0.0
            self.current_state = STATE_REFRACTORY
            self.refractory_timer = DEFAULT_REFRACTORY_TIMER
            self.last_fire_tick = current_tick
            self.fire_count += 1
            self.recent_fire_count += 1
            self.energy = max(0.0, self.energy - 10.0)
            self.synaptic_fatigue = max(0.2, self.synaptic_fatigue - 0.05)
            self.fire_threshold = max(0.5, self.fire_threshold + 0.02)
            return True

        if pre_noise_membrane >= (0.8 * self.fire_threshold):
            for connection, contribution in contributors.items():
                connection.reward_for_subthreshold()

        # Apply leak and homeostasis.
        self.membrane_potential = max(0.0, self.membrane_potential - self.decay_rate)
        self.recent_fire_count = max(0, self.recent_fire_count - 1)
        if self.recent_fire_count == 0:
            self.fire_threshold = max(0.5, self.fire_threshold - 0.01)
        if self.fire_count > 0 and self.recent_fire_count > 0:
            self.fire_threshold = max(0.5, self.fire_threshold + 0.001)
        return False

