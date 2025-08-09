"""
Reusable Parameterized Quantum Circuits (Ansatze)
"""
from qiskit.circuit.library import RealAmplitudes, EfficientSU2, TwoLocal

def create_ansatz(n_qubits, type='RealAmplitudes', reps=2):
    """
    Creates a standard parameterized quantum circuit (ansatz) from Qiskit's library.
    This is the "trainable" part of a variational algorithm.

    Args:
        n_qubits (int): The number of qubits for the ansatz.
        type (str): The type of ansatz ('RealAmplitudes', 'EfficientSU2', 'TwoLocal').
        reps (int): The number of repetitions (layers) in the ansatz, increasing its complexity.

    Returns:
        A Qiskit QuantumCircuit instance for the ansatz.
    """
    if type == 'RealAmplitudes':
        # RealAmplitudes is a simple, effective ansatz with RY rotations and CX entanglement.
        # Good for many machine learning tasks.
        return RealAmplitudes(num_qubits=n_qubits, reps=reps, entanglement='linear')
    
    elif type == 'EfficientSU2':
        # EfficientSU2 is a more expressive, hardware-efficient ansatz using single-qubit
        # rotations (SU2) and CX gates. It's a popular choice for VQEs and VQAs.
        return EfficientSU2(num_qubits=n_qubits, reps=reps, entanglement='circular')
        
    elif type == 'TwoLocal':
        # TwoLocal is a highly customizable ansatz. You can specify the rotation
        # and entanglement gates.
        return TwoLocal(num_qubits=n_qubits, rotation_blocks=['ry', 'rz'], 
                        entanglement_blocks='cx', entanglement='sca', reps=reps)

    else:
        raise ValueError(f"Unsupported ansatz type: {type}")