import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class QuantumPestForecaster:
    """
    A class to simulate pest risk forecasting using a QSVM-like approach.
    """
    def __init__(self, settings):
        self.n_qubits = 3  # QSVM for this problem is fixed to 3 qubits
        self.shots = settings.get('shots', 1024)
        self.simulator = AerSimulator()

    def _create_feature_map_circuit(self, features):
        """
        Creates a quantum circuit that encodes features into a quantum state.
        This is inspired by quantum kernel estimation.
        """
        circuit = QuantumCircuit(self.n_qubits)
        
        # Encode features using rotation gates
        for i, feature in enumerate(features):
            # Use RY and RZ gates for more complex encoding
            circuit.ry(feature * np.pi, i)
            circuit.rz(feature * np.pi * 0.5, i)

        # Entangle qubits to create complex correlations
        if self.n_qubits > 1:
            circuit.barrier()
            for i in range(self.n_qubits - 1):
                circuit.cx(i, i + 1)
        
        circuit.measure_all()
        return circuit

    def _generate_recommendations(self, risk_score, crop_stage):
        """Generates contextual recommendations based on risk."""
        recommendations = []
        if risk_score > 0.7:
            recommendations.extend([
                "**Action Required**: Immediate field inspection recommended.",
                "Deploy pheromone traps in high-risk zones.",
                "Consider targeted organic pesticide application.",
            ])
        elif risk_score > 0.4:
            recommendations.extend([
                "**Warning**: Increase monitoring frequency to daily.",
                "Focus on vulnerable crop sections (young leaves).",
                "Prepare mitigation resources.",
            ])
        else:
            recommendations.extend([
                "**All Clear**: Conditions are favorable. Continue standard monitoring.",
                "Maintain beneficial insect habitats to support natural pest control.",
            ])
        
        # Stage-specific advice
        stage_recs = {
            "Germination": "Protect seedlings with row covers if high risk is detected.",
            "Flowering": "Be cautious with any treatments to protect vital pollinators.",
            "Maturation": "Ensure proper storage plans to prevent post-harvest infestation.",
        }
        if crop_stage in stage_recs:
            recommendations.append(stage_recs[crop_stage])
        return recommendations

    def forecast(self, features):
        """
        Analyzes features to forecast pest risk.
        """
        # Ensure we have the correct number of features for our circuit
        if len(features) != self.n_qubits:
            raise ValueError(f"Expected {self.n_qubits} features, but got {len(features)}")
        
        # Normalize features to be between 0 and 1
        # [temp, humidity, rainfall] -> max values [45, 100, 100]
        normalized_features = features / np.array([45.0, 100.0, 100.0])

        circuit = self._create_feature_map_circuit(normalized_features)

        # Transpile and run the simulation
        t_circuit = transpile(circuit, self.simulator)
        result = self.simulator.run(t_circuit, shots=self.shots).result()
        counts = result.get_counts(0)

        # --- Simplified Classification Logic ---
        # A simple heuristic: more '1's in the output bitstrings suggest higher risk.
        risk_value = 0
        total_shots = sum(counts.values())
        for state, num_shots in counts.items():
            # Count the number of '1's in the state string
            num_ones = state.count('1')
            risk_value += (num_ones / self.n_qubits) * num_shots
        
        risk_score = risk_value / total_shots
        
        # Classify risk level
        if risk_score > 0.65:
            risk_level = "🔴 High Risk"
        elif risk_score > 0.35:
            risk_level = "🟡 Medium Risk"
        else:
            risk_level = "🟢 Low Risk"
        
        recommendations = self._generate_recommendations(risk_score, features[-1]) # Pass crop_stage if included

        return risk_score, risk_level, recommendations, circuit, counts