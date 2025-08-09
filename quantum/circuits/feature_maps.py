"""
Reusable Quantum Feature Maps
"""
from qiskit.circuit.library import ZZFeatureMap, PauliFeatureMap, ZFeatureMap

def create_feature_map(n_qubits, type='ZZ', reps=2):
    """
    Creates a standard quantum feature map from Qiskit's circuit library.

    Args:
        n_qubits (int): The number of qubits for the feature map.
        type (str): The type of feature map ('ZZ', 'Z', 'Pauli').
        reps (int): The number of repetitions of the feature map circuit.

    Returns:
        A Qiskit QuantumCircuit instance for the feature map.
    """
    if type == 'ZZ':
        # ZZFeatureMap is good for capturing interactions between features.
        return ZZFeatureMap(feature_dimension=n_qubits, reps=reps, entanglement='linear')
    
    elif type == 'Z':
        # ZFeatureMap is simpler and encodes features without entanglement.
        return ZFeatureMap(feature_dimension=n_qubits, reps=reps)

    elif type == 'Pauli':
        # PauliFeatureMap is more complex, using combinations of Pauli gates.
        paulis = ['Z', 'Y', 'ZZ'] # Example combination
        return PauliFeatureMap(feature_dimension=n_qubits, reps=reps, paulis=paulis)
        
    else:
        raise ValueError(f"Unsupported feature map type: {type}")