# Entry point for the SynthBio brain simulation.
#
# This script runs a single large living-brain demo with a 20-neuron network
# and richer per-tick logging so the self-organization dynamics are easier to
# follow over a longer run.

import os
import sys
import time
import termios
import tty

from brain import Brain
from world import World

SAVE_DIR = os.path.join(os.getcwd(), "saved")
SAVE_PATH = os.path.join(SAVE_DIR, "brain_state.pkl")
KEY_TICKS = {1, 5, 10, 25, 50, 100}


def describe_world_changes(brain):
    previous = brain.world.previous_values
    current = {
        "light": brain.world.light_level,
        "temperature": brain.world.temperature,
        "food": brain.world.food,
        "danger": brain.world.danger,
        "noise": brain.world.noise,
        "reward": brain.world.reward,
        "energy": brain.world.body_energy,
    }

    descriptions = []
    for key, current_value in current.items():
        previous_value = previous.get(key, current_value)
        delta = current_value - previous_value
        if abs(delta) < 0.01:
            continue

        if key == "light":
            if delta > 0:
                descriptions.append(f"light brightened ({previous_value:.2f} → {current_value:.2f})")
            else:
                descriptions.append(f"light dimmed ({previous_value:.2f} → {current_value:.2f})")
        elif key == "temperature":
            if delta > 0:
                descriptions.append(f"temperature warmed ({previous_value:.2f} → {current_value:.2f})")
            else:
                descriptions.append(f"temperature cooled ({previous_value:.2f} → {current_value:.2f})")
        elif key == "food":
            if delta > 0:
                descriptions.append(f"food increased ({previous_value:.2f} → {current_value:.2f})")
            else:
                descriptions.append(f"food dropped ({previous_value:.2f} → {current_value:.2f})")
        elif key == "danger":
            if delta > 0:
                descriptions.append(f"danger rose ({previous_value:.2f} → {current_value:.2f})")
            else:
                descriptions.append(f"danger eased ({previous_value:.2f} → {current_value:.2f})")
        elif key == "noise":
            if delta > 0:
                descriptions.append(f"noise increased ({previous_value:.2f} → {current_value:.2f})")
            else:
                descriptions.append(f"noise softened ({previous_value:.2f} → {current_value:.2f})")
        elif key == "reward":
            if delta > 0:
                descriptions.append(f"reward climbed ({previous_value:.2f} → {current_value:.2f})")
            else:
                descriptions.append(f"reward faded ({previous_value:.2f} → {current_value:.2f})")
        elif key == "energy":
            if delta > 0:
                descriptions.append(f"energy rose ({previous_value:.2f} → {current_value:.2f})")
            else:
                descriptions.append(f"energy fell ({previous_value:.2f} → {current_value:.2f})")

    if not descriptions:
        return "nothing much changed"
    return "; ".join(descriptions)


def describe_actions(actions):
    if not actions:
        return "none"

    phrases = []
    for action in actions:
        action_name = (action or "").lower()
        if action_name == "eat":
            phrases.append("ate food")
        elif action_name == "sleep":
            phrases.append("slept")
        elif action_name == "look":
            phrases.append("looked around")
        elif action_name == "grab":
            phrases.append("grabbed something")
        elif action_name == "move_left":
            phrases.append("turned left")
        elif action_name == "move_right":
            phrases.append("turned right")
        else:
            phrases.append(action_name)
    return ", ".join(phrases)


def print_compact_tick_summary(brain, tick):
    print(f"Tick {tick:03d} | World: {describe_world_changes(brain)} | Actions: {describe_actions(brain.last_actions)}")


def print_tick_snapshot(brain, tick):
    stats = brain.collect_stats()
    active_neurons = [neuron for neuron in brain.neurons if neuron.current_state == "REFRACTORY"]
    top_neurons = sorted(brain.neurons, key=lambda neuron: (neuron.fire_count, neuron.membrane_potential), reverse=True)[:6]

    print(f"Tick {tick:03d}")
    print(f"  World: {describe_world_changes(brain)}")
    print(
        f"  Actions: {describe_actions(brain.last_actions)} | "
        f"refractory={len(active_neurons)} | avg_activation={stats['average_activation']:.2f}"
    )
    strongest = stats['strongest_connection']
    strongest_label = f"{strongest.weight:.2f}" if strongest is not None else "none"
    print(
        f"  Connections: {len(brain.connections)} | avg_weight={stats['average_connection_weight']:.2f} | "
        f"strongest={strongest_label}"
    )
    print("  Top neurons:")
    for neuron in top_neurons:
        print(
            f"    n{neuron.unique_id} [{neuron.neuron_type}] state={neuron.current_state} | "
            f"membrane={neuron.membrane_potential:.2f} | fires={neuron.fire_count} | "
            f"threshold={neuron.fire_threshold:.2f}"
        )
    print(
        "  Chemistry: "
        f"dopamine={brain.chemistry['dopamine']:.2f}, serotonin={brain.chemistry['serotonin']:.2f}, "
        f"acetylcholine={brain.chemistry['acetylcholine']:.2f}, noradrenaline={brain.chemistry['noradrenaline']:.2f}"
    )
    print()


def build_scaffold_connections(brain, neurons):
    count = len(neurons)
    for index, source in enumerate(neurons):
        for offset in range(1, min(6, count)):
            target_index = (index + offset) % count
            if target_index == index:
                continue
            target = neurons[target_index]
            if any(connection.source_neuron is source and connection.target_neuron is target for connection in brain.connections):
                continue
            if len(source.outgoing_connections) >= 5:
                break
            weight = 0.42 + (0.03 * min(4, len(source.outgoing_connections)))
            signal_delay = 0 if offset <= 3 else 1
            brain.create_connection(source, target, weight=weight, signal_delay=signal_delay)


def seed_network_activity(neurons):
    for index, neuron in enumerate(neurons):
        neuron.receive(0.08 + 0.01 * (index % 4))
        neuron.membrane_potential = min(
            neuron.max_activation,
            neuron.membrane_potential + 0.05 + 0.01 * (index % 6) + (0.015 if index >= 3 else 0.0),
        )


def read_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
        if key == "\x1b":
            if sys.stdin.read(1) == "[":
                arrow = sys.stdin.read(1)
                if arrow == "A":
                    return "up"
                if arrow == "B":
                    return "down"
            return "escape"
        if key in {"\r", "\n"}:
            return "enter"
        if key == "\x03":
            return "ctrl-c"
        return key
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def prompt_startup_mode(save_path):
    options = ["Use saved model", "Start new simulation"]
    selected = 0 if os.path.exists(save_path) else 1

    if not sys.stdin.isatty():
        return "new" if not os.path.exists(save_path) else "resume"

    print("\nChoose startup mode with ↑/↓ and Enter.")
    while True:
        print("\033[2J\033[H", end="", flush=True)
        print("Choose startup mode with ↑/↓ and Enter.")
        for index, option in enumerate(options):
            marker = ">" if index == selected else " "
            suffix = "" if index == 0 or os.path.exists(save_path) else " (not available)"
            print(f"{marker} {option}{suffix}")

        key = read_key()
        if key == "up":
            selected = (selected - 1) % len(options)
        elif key == "down":
            selected = (selected + 1) % len(options)
        elif key in {"enter", " "}:
            if selected == 0 and not os.path.exists(save_path):
                print("No saved model found; starting a new simulation instead.")
                return "new"
            return "resume" if selected == 0 else "new"
        elif key == "ctrl-c":
            raise KeyboardInterrupt


def should_resume_brain_state(save_path, resume=False):
    return resume and os.path.exists(save_path)


def run_living_brain_demo(save_path=SAVE_PATH, max_ticks=None, resume=False):
    should_resume = should_resume_brain_state(save_path, resume)
    os.makedirs(SAVE_DIR, exist_ok=True)

    if should_resume:
        print(f"Resuming brain from {save_path}")
        brain = Brain.load(save_path)
    else:
        if os.path.exists(save_path):
            print(f"Starting fresh; ignoring existing save at {save_path}")
        brain = Brain(world=World(food=6.0, reward=1.0, body_energy=70.0))

        sensor_names = ["light", "food", "temperature"]
        sensors = []
        for sensor_name in sensor_names:
            neuron = brain.create_neuron(output_strength=0.6, fire_threshold=0.75, neuron_type="SENSORY", excitatory=True)
            brain.register_sensor(neuron, sensor_name)
            sensors.append(neuron)

        hidden_neurons = []
        for index in range(10):
            neuron = brain.create_neuron(
                output_strength=0.55 + (index % 4) * 0.05,
                fire_threshold=0.82 + (index % 3) * 0.06,
                neuron_type="NORMAL",
                excitatory=index % 3 != 0,
            )
            hidden_neurons.append(neuron)

        output_neurons = []
        for index in range(4):
            neuron = brain.create_neuron(output_strength=0.75, fire_threshold=0.70, neuron_type="OUTPUT", excitatory=True)
            output_neurons.append(neuron)

        specialist_neurons = []
        for neuron_type in ["MEMORY", "REWARD", "PACEMAKER"]:
            specialist_neurons.append(
                brain.create_neuron(output_strength=0.7, fire_threshold=0.75, neuron_type=neuron_type, excitatory=True)
            )

        all_neurons = sensors + hidden_neurons + output_neurons + specialist_neurons
        assert len(all_neurons) == 20

        build_scaffold_connections(brain, all_neurons)
        seed_network_activity(all_neurons)

    print("=== Living brain demo ===")
    print("Persistent brain simulation — save/resume enabled and structural changes are active.")

    max_ticks_env = os.environ.get("SYNTHBIO_MAX_TICKS", "")
    if max_ticks is None:
        max_ticks = int(max_ticks_env) if max_ticks_env.isdigit() else None

    try:
        while True:
            brain.tick()
            tick = brain.current_tick
            print_compact_tick_summary(brain, tick)
            if tick in KEY_TICKS:
                print_tick_snapshot(brain, tick)
                brain.print_brain_report()
            if tick % 25 == 0:
                brain.save(save_path)
                print(f"Saved brain state to {save_path}")
            if max_ticks is not None and tick >= max_ticks:
                break
            time.sleep(0.2)
    except KeyboardInterrupt:
        brain.save(save_path)
        print(f"Saved brain state to {save_path} before exit.")

    print("Living brain demo complete.")


def main():
    startup_mode = prompt_startup_mode(SAVE_PATH)
    run_living_brain_demo(resume=startup_mode == "resume")


if __name__ == "__main__":
    main()
