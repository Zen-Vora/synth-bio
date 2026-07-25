# Entry point for the SynthBio brain simulation.
#
# This script creates a brain with five neurons plus an input neuron.
# The input neuron receives explicit test signals, and the brain only
# coordinates ticks, signal delivery, and neuron updates.

from brain import Brain


def run_competition_demo():
    brain = Brain()

    # Build the competition topology: 0 -> {1,2} -> 3.
    input_neuron = brain.create_neuron(output_strength=1.0, fire_threshold=0.5, neuron_type="INPUT")
    neuron_1 = brain.create_neuron(output_strength=0.8, fire_threshold=0.5, neuron_type="NORMAL")
    neuron_2 = brain.create_neuron(output_strength=0.8, fire_threshold=0.5, neuron_type="NORMAL")
    neuron_3 = brain.create_neuron(output_strength=0.8, fire_threshold=0.8, neuron_type="NORMAL")

    brain.create_connection(source_neuron=input_neuron, target_neuron=neuron_1, weight=0.50, signal_delay=1)
    brain.create_connection(source_neuron=input_neuron, target_neuron=neuron_2, weight=0.50, signal_delay=1)
    brain.create_connection(source_neuron=neuron_1, target_neuron=neuron_3, weight=0.50, signal_delay=1)
    brain.create_connection(source_neuron=neuron_2, target_neuron=neuron_3, weight=0.50, signal_delay=1)

    print("=== Competition experiment ===")
    print("Training branch 1 first by repeatedly stimulating neuron 1.")

    for tick in range(1, 16):
        if tick in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}:
            if tick <= 8:
                neuron_1.receive(1.0)
            else:
                neuron_2.receive(1.0)

        brain.tick()

        if tick in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}:
            print(f"Tick {tick}")
            brain.print_stats()
            for neuron in brain.neurons:
                print(
                    f"  Neuron {neuron.unique_id}: activation={neuron.current_activation:.2f}, "
                    f"state={neuron.current_state}, type={neuron.neuron_type}, "
                    f"fire_count={neuron.fire_count}"
                )
            print("Connection weights:")
            for connection in brain.connections:
                print(
                    f"  {connection.source_neuron.unique_id} -> {connection.target_neuron.unique_id}: "
                    f"{connection.weight:.2f}"
                )
            print()

    print("Competition training complete.")


def run_repeated_training_demo():
    brain = Brain()

    input_neuron = brain.create_neuron(output_strength=1.0, fire_threshold=0.5, neuron_type="INPUT")
    neuron_a = brain.create_neuron(output_strength=0.8, fire_threshold=0.5, neuron_type="NORMAL")
    neuron_b = brain.create_neuron(output_strength=0.8, fire_threshold=0.8, neuron_type="NORMAL")

    brain.create_connection(source_neuron=input_neuron, target_neuron=neuron_a, weight=0.50, signal_delay=1)
    brain.create_connection(source_neuron=neuron_a, target_neuron=neuron_b, weight=0.50, signal_delay=1)

    print("=== Repeated training experiment ===")
    print("Pulsing the input every few ticks.")

    for tick in range(1, 13):
        if tick in {1, 4, 7, 10}:
            input_neuron.receive(1.0)

        brain.tick()

        if tick in {1, 4, 7, 10}:
            print(f"Tick {tick}")
            brain.print_stats()
            for connection in brain.connections:
                print(
                    f"  {connection.source_neuron.unique_id} -> {connection.target_neuron.unique_id}: "
                    f"{connection.weight:.2f}"
                )
            print()

    print("Repeated training complete.")


def main():
    run_competition_demo()
    run_repeated_training_demo()


if __name__ == "__main__":
    main()
