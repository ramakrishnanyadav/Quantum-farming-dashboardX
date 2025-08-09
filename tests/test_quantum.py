import unittest
from quantum.algorithms.irrigation_optimizer import QuantumIrrigationOptimizer

class TestQuantumAlgorithms(unittest.TestCase):

    def setUp(self):
        """Set up a mock settings dictionary for testing."""
        self.settings = {
            'n_qubits': 4,
            'circuit_depth': 1,
            'shots': 128,
            'backend_type': 'Simulator'
        }

    def test_irrigation_optimizer_runs(self):
        """
        Test that the irrigation optimizer runs without errors and returns correct types.
        """
        optimizer = QuantumIrrigationOptimizer(self.settings)
        
        # Mock zone data
        zone_data = [{'requirement': 1000} for _ in range(self.settings['n_qubits'])]
        
        allocation, counts, circuit = optimizer.optimize(zone_data)
        
        self.assertEqual(len(allocation), self.settings['n_qubits'])
        self.assertIsInstance(counts, dict)
        # Check if the highest probability is a 4-bit string
        self.assertEqual(len(max(counts, key=counts.get)), self.settings['n_qubits'])

if __name__ == '__main__':
    unittest.main()