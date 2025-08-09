"""
Quantum algorithm hyperparameters and backend configurations.
"""

# Quantum Circuit Parameters
YIELD_PREDICTOR_CONFIG = {
    'n_qubits': 4,
    'ansatz_reps': 2,
    'feature_map_reps': 2,
    'optimizer': 'SPSA',
    'max_iter': 80
}

IRRIGATION_OPTIMIZER_CONFIG = {
    'max_zones': 8,
    'qaoa_reps': 2, # 'p' value for QAOA
    'optimizer': 'COBYLA',
    'max_iter': 100
}

PEST_FORECASTER_CONFIG = {
    'n_qubits': 3,
    'feature_map_reps': 2,
    'classification_threshold': 0.5
}