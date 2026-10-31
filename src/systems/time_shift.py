# src/systems/time_shift.py
from src.config import EPOCH_PRESENT, EPOCH_PAST, EPOCH_FUTURE

class TimeShiftSystem:
    def __init__(self):
        self.current_epoch = EPOCH_PRESENT

    def shift_epoch(self, epoch_id):
        if epoch_id in [EPOCH_PRESENT, EPOCH_PAST, EPOCH_FUTURE]:
            self.current_epoch = epoch_id
            return True
        return False

    def cycle(self):
        self.current_epoch = (self.current_epoch + 1) % 3
        return self.current_epoch