# Connection module for the SynthBio brain simulation.
#
# This module defines the Connection class, which knows its source and target
# neurons, applies weight, handles delay, and carries a signal from source to target.


class Connection:
    # A connection links a source neuron to a target neuron.
    # It carries a weighted signal and respects delay.
    def __init__(
        self,
        unique_id,
        source_neuron,
        target_neuron,
        weight=1.0,
        signal_delay=0,
        enabled=True,
    ):
        # Unique identifier for the connection.
        self.unique_id = unique_id
        # Neuron that emits signals along this connection.
        self.source_neuron = source_neuron
        # Neuron that receives signals from this connection.
        self.target_neuron = target_neuron
        # Weight multiplier applied to signal strength.
        self.weight = weight
        # Delay in ticks before the signal arrives at the target neuron.
        self.signal_delay = signal_delay
        # Whether this connection currently carries signals.
        self.enabled = enabled
        # Tick when the source neuron most recently fired. Used for STDP,
        # which cares about causal timing between source and target spikes.
        self.last_source_fire_tick = None
        # Tick when this connection last actually carried a delivered
        # signal. Used for staleness-based pruning -- distinct from
        # last_source_fire_tick because a disabled connection's source can
        # still fire without the connection itself doing anything useful.
        self.last_activity_tick = None
        # Pending signals waiting to arrive at the target neuron.
        self.pending_signals = []

    def record_source_fire(self, current_tick):
        # Remember when the source neuron fired so the connection can learn.
        self.last_source_fire_tick = current_tick

    def apply_stdp(self, current_tick):
        # Adjust connection strength based on causal spike timing.
        if self.last_source_fire_tick is None:
            return

        time_difference = current_tick - self.last_source_fire_tick
        if time_difference <= 0:
            self.weight = max(0.0, self.weight - 0.01)
            return

        if time_difference == 1:
            self.weight = min(1.0, self.weight + 0.08)
        elif time_difference == 2:
            self.weight = min(1.0, self.weight + 0.04)
        else:
            self.weight = max(0.0, self.weight - 0.02)

    def reward_for_spike(self):
        # Reward the connection strongly when it helped a neuron fire.
        self.weight = min(1.0, self.weight + 0.12)

    def reward_for_subthreshold(self):
        # Reward the connection a little when it helped push a neuron close to firing.
        self.weight = min(1.0, self.weight + 0.03)

    def transmit(self, signal_strength, current_tick):
        # Begin transmitting a new signal along this connection.
        if not self.enabled:
            return

        effective_signal = signal_strength * self.weight
        if hasattr(self.source_neuron, "synaptic_fatigue"):
            effective_signal *= self.source_neuron.synaptic_fatigue
        # Dale's Law: a neuron's excitatory/inhibitory identity is a property
        # of the SENDER and applies to every target it connects to. This is
        # the one place that sign gets applied -- neuron.py no longer touches
        # it on the receiving end.
        if hasattr(self.source_neuron, "excitatory") and not self.source_neuron.excitatory:
            effective_signal = -effective_signal
        self.pending_signals.append((current_tick + self.signal_delay, effective_signal))
        self.last_activity_tick = current_tick

    def advance(self, current_tick):
        # Deliver any signals whose arrival tick has arrived.
        delivered_signals = []
        remaining_signals = []
        for arrival_tick, signal_value in self.pending_signals:
            if arrival_tick <= current_tick:
                delivered_signals.append(signal_value)
            else:
                remaining_signals.append((arrival_tick, signal_value))
        self.pending_signals = remaining_signals
        return delivered_signals
