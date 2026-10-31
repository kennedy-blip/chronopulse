# src/systems/adrenaline.py
class AdrenalineSystem:
    def __init__(self, max_value=100.0, decay_rate=5.0):
        self.value = 0.0
        self.max_value = max_value
        self.decay_rate = decay_rate
        self.is_overdrive = False

    def update(self, dt, is_running_fast=True):
        if is_running_fast:
            self.value += 15.0 * dt
        else:
            self.value -= self.decay_rate * dt

        self.value = max(0.0, min(self.value, self.max_value))
        self.is_overdrive = (self.value >= self.max_value)

    def add_boost(self, amount):
        self.value = min(self.value + amount, self.max_value)