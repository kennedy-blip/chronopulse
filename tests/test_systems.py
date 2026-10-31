# tests/test_systems.py
import unittest
import os
import sys

# Add project root directory to path for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.systems.adrenaline import AdrenalineSystem
from src.systems.time_shift import TimeShiftSystem
from src.database.db_manager import init_db, save_run, get_high_score

class TestChronopulseSystems(unittest.TestCase):
    
    def setUp(self):
        init_db()

    def test_adrenaline_buildup(self):
        adrenaline = AdrenalineSystem(max_value=100.0, decay_rate=5.0)
        self.assertEqual(adrenaline.value, 0.0)
        
        for _ in range(10):
            adrenaline.update(0.1, is_running_fast=True)
            
        self.assertGreater(adrenaline.value, 0.0)
        self.assertLessEqual(adrenaline.value, 100.0)

    def test_adrenaline_overdrive(self):
        adrenaline = AdrenalineSystem(max_value=50.0)
        adrenaline.add_boost(60.0)
        self.assertEqual(adrenaline.value, 50.0)
        self.assertTrue(adrenaline.is_overdrive)

    def test_time_shift_cycling(self):
        time_sys = TimeShiftSystem()
        self.assertEqual(time_sys.current_epoch, 0)
        
        epoch = time_sys.cycle()
        self.assertEqual(epoch, 1)
        
        epoch = time_sys.cycle()
        self.assertEqual(epoch, 2)
        
        epoch = time_sys.cycle()
        self.assertEqual(epoch, 0)

    def test_database_high_score(self):
        save_run(120, 0)
        save_run(450, 2)
        
        high_score = get_high_score()
        self.assertEqual(high_score, 450)

if __name__ == '__main__':
    unittest.main()