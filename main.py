# Entry point for the SynthBio brain simulation.
#
# This script creates a brain with five neurons plus an input neuron.
# The input neuron receives explicit test signals, and the brain only
# coordinates ticks, signal delivery, and neuron updates.

from brain import Brain


def main():
    brain = Brain()

    # Create an explicit input neuron that represents the environment.
    input_neuron = brain.create_neuron(
        output_strength=1.0,
        fire_threshold=1.0,
        neuron_type="INPUT",
    )
    neuron_a = brain.create_neuron(
        output_strength=0.8,
        fire_threshold=1.0,
        neuron_type="NORMAL",
    )
    neuron_b = brain.create_neuron(
        output_strength=0.8,
        fire_threshold=1.0,
        neuron_type="NORMAL",
    )
    neuron_c = brain.create_neuron(
        output_strength=0.8,
        fire_threshold=1.0,
        neuron_type="NORMAL",
    )
    neuron_d = brain.create_neuron(
        output_strength=0.8,
        fire_threshold=1.0,
        neuron_type="NORMAL",
    )
    neuron_e = brain.create_neuron(
        output_strength=0.8,
        fire_threshold=1.0,
        neuron_type="OUTPUT",
    )

    # Wire the input neuron into the network.
    brain.create_connection(source_neuron=input_neuron, target_neuron=neuron_a, weight=1.0, signal_delay=1)
    brain.create_connection(source_neuron=neuron_a, target_neuron=neuron_b, weight=1.0, signal_delay=1)
    brain.create_connection(source_neuron=neuron_b, target_neuron=neuron_c, weight=1.0, signal_delay=1)
    brain.create_connection(source_neuron=neuron_c, target_neuron=neuron_d, weight=1.0, signal_delay=1)
    brain.create_connection(source_neuron=neuron_d, target_neuron=neuron_e, weight=1.0, signal_delay=1)

    # Send a test signal into the input neuron.
    input_neuron.receive(1.0)

    # Display the current network before simulation.
    print("\n--- connection graph ---\n")
    brain.inspect_network()
    print()

    # Run the simulation for a few ticks.
    for tick_count in range(6):
        brain.tick()
        print(f"Tick {brain.current_tick}")
        for neuron in brain.neurons:
            print(
                f"  Neuron {neuron.unique_id}: activation={neuron.current_activation:.2f}, "
                f"state={neuron.current_state}, type={neuron.neuron_type}, "
                f"refractory={neuron.refractory_timer}, "
                f"last_fire={neuron.last_fire_tick}, fire_count={neuron.fire_count}"
            )
        print("Connection graph:")
        brain.inspect_network()
        print("Firing graph:")
        brain.visualize()
        print()


if __name__ == "__main__":
    main()
