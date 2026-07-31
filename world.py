# World module for the SynthBio living-brain simulation.
#
# The world is a lightweight environment that changes over time and responds
# to the actions produced by the brain. It is intentionally simple so the
# focus stays on the loop: world -> sensory neurons -> brain -> motor neurons -> world.

import random


class World:
    def __init__(
        self,
        light_level=0.5,
        temperature=0.5,
        food=5.0,
        danger=0.2,
        noise=0.1,
        reward=0.0,
        body_energy=50.0,
    ):
        self.light_level = float(light_level)
        self.temperature = float(temperature)
        self.food = float(food)
        self.danger = float(danger)
        self.noise = float(noise)
        self.reward = float(reward)
        self.body_energy = float(body_energy)
        self.previous_values = {
            "light": self.light_level,
            "temperature": self.temperature,
            "food": self.food,
            "danger": self.danger,
            "noise": self.noise,
            "reward": self.reward,
            "body_energy": self.body_energy,
        }

    def tick(self):
        # The world changes a little each tick, even without input.
        # This creates a weak background drift that sensory neurons can detect.
        self.previous_values = {
            "light": self.light_level,
            "temperature": self.temperature,
            "food": self.food,
            "danger": self.danger,
            "noise": self.noise,
            "reward": self.reward,
            "body_energy": self.body_energy,
        }

        self.light_level = max(0.0, min(1.0, self.light_level + random.uniform(-0.1, 0.1)))
        self.temperature = max(0.0, min(1.0, self.temperature + random.uniform(-0.08, 0.08)))
        self.food = max(0.0, self.food - 0.05)
        self.danger = max(0.0, min(1.0, self.danger + random.uniform(-0.03, 0.03)))
        self.noise = max(0.0, min(1.0, self.noise + random.uniform(-0.05, 0.05)))
        self.reward = max(0.0, self.reward - 0.02)
        self.body_energy = max(0.0, min(100.0, self.body_energy - 0.1))

    def get_sensor_signal(self, name):
        # Sensory neurons should respond to both current state and change.
        current_value = getattr(self, self._attribute_name(name), None)
        previous_value = self.previous_values.get(name, current_value)
        if current_value is None:
            return 0.0

        scales = {
            "light": 1.0,
            "temperature": 1.0,
            "food": 10.0,
            "danger": 1.0,
            "noise": 1.0,
            "reward": 10.0,
            "body_energy": 100.0,
        }
        scale = scales.get(name, 1.0)
        normalized_current = current_value / scale
        normalized_change = (current_value - previous_value) / scale
        return max(0.0, 0.7 * normalized_current + 0.3 * normalized_change)

    def _attribute_name(self, name):
        mapping = {
            "light": "light_level",
            "temperature": "temperature",
            "food": "food",
            "danger": "danger",
            "noise": "noise",
            "reward": "reward",
            "body_energy": "body_energy",
        }
        return mapping.get(name, name)

    def apply_action(self, action):
        # Actions change the world and therefore create new sensations.
        action = (action or "").lower()
        if action == "eat":
            self.food = max(0.0, self.food - 1.5)
            self.body_energy = min(100.0, self.body_energy + 8.0)
            self.reward = min(10.0, self.reward + 2.0)
        elif action == "sleep":
            self.body_energy = min(100.0, self.body_energy + 6.0)
            self.danger = max(0.0, self.danger - 0.2)
        elif action == "look":
            self.reward = min(10.0, self.reward + 0.5)
            self.noise = min(1.0, self.noise + 0.05)
        elif action == "grab":
            self.food = min(10.0, self.food + 2.0)
            self.reward = min(10.0, self.reward + 1.0)
        elif action == "move_left":
            self.light_level = max(0.0, min(1.0, self.light_level + 0.1))
            self.noise = min(1.0, self.noise + 0.05)
        elif action == "move_right":
            self.light_level = max(0.0, min(1.0, self.light_level - 0.1))
            self.noise = min(1.0, self.noise + 0.05)
        else:
            self.reward = max(0.0, self.reward - 0.1)
