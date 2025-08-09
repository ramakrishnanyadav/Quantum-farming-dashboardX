import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class QuantumIrrigationOptimizer:
    """
    A class to handle irrigation optimization using a simulated QAOA.
    """
    def __init__(self, settings):
        self.n_qubits = settings.get('n_qubits', 5) # Default to 5 zones
        self.depth = settings.get('circuit_depth', 2) # Corresponds to QAOA reps (p)
        self.shots = settings.get('shots', 1024)
        self.simulator = AerSimulator()

    def _create_qaoa_circuit(self, n_qubits):
        """
        Creates a simplified QAOA circuit for demonstration.

        In a real QAOA, the angles (beta, gamma) would be optimized by a classical
        optimizer. For this hackathon, we use fixed angles for speed.
        """
        circuit = QuantumCircuit(n_qubits)
        
        # Initial superposition
        circuit.h(range(n_qubits))
        circuit.barrier()

        # Apply cost and mixer layers 'p' (depth) times
        for _ in range(self.depth):
            # Cost Hamiltonian (problem-specific) - simplified with ZZ interactions
            for i in range(n_qubits - 1):
                circuit.rzz(np.pi / 2, i, i + 1)
            circuit.barrier()
            
            # Mixer Hamiltonian (standard)
            circuit.rx(np.pi / 3, range(n_qubits))
            circuit.barrier()

        circuit.measure_all()
        return circuit

    def optimize(self, zone_data):
        """
        Runs the QAOA simulation to find an optimal irrigation schedule.
        """
        n_zones = len(zone_data)
        
        # Create the quantum circuit
        circuit = self._create_qaoa_circuit(n_zones)

        # Transpile and run the simulation
        t_circuit = transpile(circuit, self.simulator)
        result = self.simulator.run(t_circuit, shots=self.shots).result()
        counts = result.get_counts(0)

        # Find the most probable quantum state (our "optimal" solution)
        best_state = max(counts, key=counts.get)
        
        # --- Simplified Post-Processing ---
        # Map the 'best_state' bitstring to a water allocation strategy.
        # '1' means irrigate, '0' means don't.
        # This heuristic can be made much more complex.
        optimal_allocation = [
            zone['requirement'] * 0.8 if bit == '1' else 0
            for zone, bit in zip(zone_data, best_state)
        ]

        return optimal_allocation, counts, circuit