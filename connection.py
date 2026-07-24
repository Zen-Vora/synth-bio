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

    def transmit(self, signal_strength):
        # Begin transmitting a new signal along this connection.
        if not self.enabled:
            return

        self._pending_signal = signal_strength * self.weight
        self._remaining_travel_time = self.signal_delay

    def advance(self):
        # Move a traveling signal one tick closer to its target.
        pending_signal = getattr(self, "_pending_signal", None)
        remaining_time = getattr(self, "_remaining_travel_time", None)
        if pending_signal is None or remaining_time is None:
            return None

        self._remaining_travel_time -= 1
        if self._remaining_travel_time <= 0:
            delivered_signal = self._pending_signal
            del self._pending_signal
            del self._remaining_travel_time
            return delivered_signal

        return None
