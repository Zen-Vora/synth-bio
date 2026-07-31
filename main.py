# Entry point for the SynthBio brain simulation.
#
# This script creates a brain with five neurons plus an input neuron.
# The input neuron receives explicit test signals, and the brain only
# coordinates ticks, signal delivery, and neuron updates.

from brain import Brain
from world import World


def run_competition_demo():
    brain = Brain()

    input_neuron = brain.create_neuron(
        output_strength=1.0,
        fire_threshold=0.8,
        neuron_type="INPUT",
        excitatory=True,
    )
    neuron_1 = brain.create_neuron(
        output_strength=0.8,
        fire_threshold=0.9,
        neuron_type="NORMAL",
        excitatory=True,
    )
    neuron_2 = brain.create_neuron(
        output_strength=0.8,
        fire_threshold=1.1,
        neuron_type="NORMAL",
        excitatory=True,
    )
    neuron_3 = brain.create_neuron(
        output_strength=0.8,
        fire_threshold=1.0,
        neuron_type="NORMAL",
        excitatory=False,
    )

    brain.create_connection(source_neuron=input_neuron, target_neuron=neuron_1, weight=0.50, signal_delay=1)
    brain.create_connection(source_neuron=input_neuron, target_neuron=neuron_2, weight=0.50, signal_delay=1)
    brain.create_connection(source_neuron=neuron_1, target_neuron=neuron_3, weight=0.50, signal_delay=1)
    brain.create_connection(source_neuron=neuron_2, target_neuron=neuron_3, weight=0.50, signal_delay=1)

    print("=== Competition experiment ===")
    print("Training branch 1 first, then branch 2, to see how inhibitory balance changes the dynamics.")

    for tick in range(1, 11):
        if tick <= 5:
            neuron_1.receive(1.0)
        else:
            neuron_2.receive(1.0)

        brain.tick()
        print(f"Tick {tick}")
        brain.print_stats()
        for neuron in brain.neurons:
            print(
                f"  Neuron {neuron.unique_id}: membrane={neuron.current_activation:.2f}, "
                f"state={neuron.current_state}, type={neuron.neuron_type}, "
                f"fire_count={neuron.fire_count}, threshold={neuron.fire_threshold:.2f}"
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

    input_neuron = brain.create_neuron(
        output_strength=1.0,
        fire_threshold=0.8,
        neuron_type="INPUT",
        excitatory=True,
    )
    neuron_a = brain.create_neuron(
        output_strength=0.8,
        fire_threshold=0.9,
        neuron_type="NORMAL",
        excitatory=True,
    )
    neuron_b = brain.create_neuron(
        output_strength=0.8,
        fire_threshold=1.1,
        neuron_type="NORMAL",
        excitatory=False,
    )

    brain.create_connection(source_neuron=input_neuron, target_neuron=neuron_a, weight=0.50, signal_delay=1)
    brain.create_connection(source_neuron=neuron_a, target_neuron=neuron_b, weight=0.50, signal_delay=1)

    print("=== Repeated training experiment ===")
    print("Pulsing the input every few ticks to observe the effect of inhibitory feedback.")

    for tick in range(1, 11):
        if tick in {1, 4, 7, 10}:
            input_neuron.receive(1.0)

        brain.tick()
        print(f"Tick {tick}")
        brain.print_stats()
        for connection in brain.connections:
            print(
                f"  {connection.source_neuron.unique_id} -> {connection.target_neuron.unique_id}: "
                f"{connection.weight:.2f}"
            )
        print()

    print("Repeated training complete.")


def run_living_brain_demo():
    brain = Brain(world=World(food=6.0, reward=1.0, body_energy=70.0))

    light_sensor = brain.create_neuron(output_strength=0.5, fire_threshold=0.8, neuron_type="SENSORY")
    food_sensor = brain.create_neuron(output_strength=0.5, fire_threshold=0.8, neuron_type="SENSORY")
    temp_sensor = brain.create_neuron(output_strength=0.5, fire_threshold=0.8, neuron_type="SENSORY")

    hidden = brain.create_neuron(output_strength=0.7, fire_threshold=0.6, neuron_type="NORMAL", excitatory=True)
    eater = brain.create_neuron(output_strength=1.0, fire_threshold=0.5, neuron_type="OUTPUT", excitatory=True)
    sleeper = brain.create_neuron(output_strength=1.0, fire_threshold=0.5, neuron_type="OUTPUT", excitatory=True)

    brain.register_sensor(light_sensor, "light")
    brain.register_sensor(food_sensor, "food")
    brain.register_sensor(temp_sensor, "temperature")

    brain.create_connection(light_sensor, hidden, weight=0.6, signal_delay=0)
    brain.create_connection(food_sensor, hidden, weight=0.8, signal_delay=0)
    brain.create_connection(temp_sensor, hidden, weight=0.5, signal_delay=0)
    brain.create_connection(hidden, eater, weight=0.7, signal_delay=0)
    brain.create_connection(hidden, sleeper, weight=0.6, signal_delay=0)

    print("=== Living brain demo ===")
    print("A small sensory-to-action loop where world changes drive the network and actions feed back into the world.")

    for tick in range(1, 16):
        brain.tick()
        print(f"Tick {tick}")
        print(
            f"World: light={brain.world.light_level:.2f}, temp={brain.world.temperature:.2f}, "
            f"food={brain.world.food:.2f}, reward={brain.world.reward:.2f}, energy={brain.world.body_energy:.2f}"
        )
        if brain.last_actions:
            print(f"Actions: {', '.join(brain.last_actions)}")
        for neuron in brain.neurons:
            print(
                f"  Neuron {neuron.unique_id}: state={neuron.current_state}, "
                f"membrane={neuron.membrane_potential:.2f}, energy={neuron.energy:.1f}, "
                f"fires={neuron.fire_count}"
            )
        print()

    print("Living brain demo complete.")


def main():
    run_competition_demo()
    run_repeated_training_demo()
    run_living_brain_demo()


if __name__ == "__main__":
    main()
