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
    ):
        # Unique identifier for this neuron.
        self.unique_id = unique_id
        # Current total activation level of the neuron.
        self.current_activation = current_activation
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

    def receive(self, signal_strength):
        # Accept a signal and store it in the neuron's input buffer.
        self.input_buffer.append(signal_strength)

    def update(self, current_tick):
        # A neuron decides whether it fires based on its own state and activation.
        if self.current_state == STATE_REFRACTORY:
            # Refractory neurons ignore input and count down.
            self.refractory_timer -= 1
            if self.refractory_timer <= 0:
                self.current_state = STATE_RESTING
            return False

        # Integrate all buffered input signals into activation.
        total_input = sum(self.input_buffer)
        self.input_buffer.clear()
        self.current_activation += total_input

        # Enforce the maximum activation cap.
        if self.current_activation > self.max_activation:
            self.current_activation = self.max_activation

        # Decide whether the neuron fires this tick.
        if self.current_activation >= self.fire_threshold:
            self.current_activation = 0.0
            self.current_state = STATE_REFRACTORY
            self.refractory_timer = DEFAULT_REFRACTORY_TIMER
            self.last_fire_tick = current_tick
            self.fire_count += 1
            return True

        # Apply activation decay toward baseline when the neuron does not fire.
        self.current_activation = max(0.0, self.current_activation - self.decay_rate)
        return False

