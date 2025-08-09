# Quantum Algorithms API Documentation

## Overview

This document describes the quantum algorithms implemented in the Quantum Smart Farming Dashboard, their parameters, and expected outputs.

## Variational Quantum Regressor (VQR)

### Purpose
Predicts crop yield based on environmental factors using quantum machine learning.

### Input Parameters
```python
{
    "temperature": float,    # °C (e.g., 31.0)
    "humidity": float,       # % (e.g., 70.0) 
    "soil_ph": float,        # pH units (e.g., 6.5)
    "rainfall": float,       # mm (e.g., 25.4)
    "fertilizer": float      # kg/hectare (e.g., 150.0)
}
```

### Quantum Circuit Configuration
```python
{
    "n_qubits": 4,           # Range: 2-6
    "circuit_depth": 3,      # Range: 1-5
    "quantum_shots": 1024,   # Range: 512-4096
    "feature_map": "ZZFeatureMap",
    "ansatz": "RealAmplitudes",
    "optimizer": "SPSA"
}
```

### Output
```python
{
    "predicted_yield": 8.27,    # tons/hectare
    "confidence": 0.94,         # prediction confidence
    "quantum_fidelity": 0.892,  # circuit execution fidelity
    "execution_time": 2.3       # seconds
}
```

## Quantum Approximate Optimization Algorithm (QAOA)

### Purpose
Optimizes irrigation schedules to minimize water usage while maintaining crop health.

### Input Parameters
```python
{
    "farm_zones": int,           # Number of irrigation zones
    "water_budget": float,       # Total water available (liters)
    "crop_requirements": dict,   # Water needs per crop type
    "soil_capacity": dict,       # Water retention per zone
    "weather_forecast": dict     # 5-day precipitation forecast
}
```

### Quantum Configuration
```python
{
    "n_qubits": 3,              # Fixed for current implementation
    "qaoa_layers": 2,           # p parameter
    "mixer_operator": "X",      # Mixing Hamiltonian
    "cost_operator": "Custom"   # Problem-specific Hamiltonian
}
```

### Output
```python
{
    "irrigation_schedule": dict,  # Zone-wise water allocation
    "water_savings": 15.2,       # Percentage reduction
    "risk_factors": dict,        # Zone-wise risk assessment
    "optimization_score": 0.87   # Solution quality
}
```

## Quantum Support Vector Machine (QSVM)

### Purpose
Classifies pest outbreak risk based on environmental conditions and historical data.

### Input Parameters
```python
{
    "temperature_trend": list,   # 7-day temperature history
    "humidity_levels": list,     # 7-day humidity data
    "crop_stage": str,          # Growth phase
    "previous_outbreaks": dict,  # Historical pest data
    "treatment_history": list    # Previous interventions
}
```

### Quantum Configuration
```python
{
    "n_qubits": 3,              # Feature encoding qubits
    "feature_map_reps": 2,      # Feature map repetitions
    "kernel_type": "RBF",       # Quantum kernel
    "training_size": 100        # Training dataset size
}
```

### Output
```python
{
    "risk_level": "High",       # High/Low classification
    "probability": 0.78,        # Outbreak probability
    "confidence": 0.94,         # Classification confidence
    "risk_factors": dict,       # Contributing factors
    "recommendations": list     # Suggested actions
}
```

## API Usage Examples

### VQR Prediction Example
```python
from quantum.algorithms.yield_predictor import QuantumYieldPredictor

# Initialize predictor
predictor = QuantumYieldPredictor(n_qubits=4, n_layers=3)

# Prepare input data
input_data = {
    "temperature": 31.0,
    "humidity": 70.0,
    "soil_ph": 6.5,
    "rainfall": 15.2,
    "fertilizer": 120.0
}

# Run prediction
result = predictor.predict(input_data)
print(f"Predicted yield: {result['predicted_yield']:.2f} tons/hectare")
```

### QAOA Optimization Example
```python
from quantum.algorithms.irrigation_optimizer import QuantumIrrigationOptimizer

# Initialize optimizer
optimizer = QuantumIrrigationOptimizer(n_zones=3, p_layers=2)

# Set constraints
constraints = {
    "water_budget": 10000,  # liters
    "zone_requirements": [2000, 3000, 2500],
    "soil_capacity": [0.8, 0.6, 0.9]
}

# Optimize schedule
schedule = optimizer.optimize(constraints)
print(f"Water savings: {schedule['water_savings']:.1f}%")
```

## Error Handling

### Common Quantum Errors
```python
# Circuit compilation failure
QuantumCircuitError: "Circuit depth too large for backend"
# Solution: Reduce circuit_depth parameter

# Backend connection timeout  
BackendError: "Quantum backend unavailable"
# Solution: Switch to 'aer_simulator' backend

# Insufficient quantum shots
ShotError: "Not enough shots for reliable results"
# Solution: Increase quantum_shots parameter (min 512)
```

## Performance Optimization

### Best Practices
- **Circuit Depth**: Keep ≤ 5 layers for simulator performance
- **Quantum Shots**: Use 1024+ for production, 512 for testing
- **Caching**: Enable result caching for repeated predictions
- **Batch Processing**: Group similar predictions for efficiency

### Benchmarks
| Operation | Avg Time | Memory Usage |
|-----------|----------|--------------|
| VQR Training | 15-30s | 150MB |
| VQR Prediction | 2-5s | 50MB |
| QAOA Optimization | 10-20s | 100MB |
| QSVM Classification | 3-8s | 75MB |

## Quantum Backend Configuration

### Simulator (Recommended for Development)
```python
backend_config = {
    "backend_name": "aer_simulator",
    "shots": 1024,
    "optimization_level": 1,
    "memory": True
}
```

### Real Quantum Device (Production)
```python
backend_config = {
    "backend_name": "ibm_brisbane",  # or available device
    "shots": 512,
    "optimization_level": 3,
    "error_mitigation": True
}
```

## Testing Guidelines

### Unit Tests
```python
# Test quantum algorithms
pytest tests/test_quantum.py::test_vqr_prediction

# Test data integration
pytest tests/test_api.py::test_weather_collection

# Test full pipeline
pytest tests/test_integration.py
```

### Integration Tests
```python
# Test with real APIs (use test keys)
pytest tests/integration/ --api-tests

# Test quantum circuits
pytest tests/quantum/ --slow
```

## Support

- **💬 Questions**: [GitHub Discussions](https://github.com/ramakrishnanyadav/quantum-farming-dashboard/discussions)
- **🐛 Bug Reports**: [GitHub Issues](https://github.com/ramakrishnanyadav/quantum-farming-dashboard/issues)
- **📧 Direct Contact**: ramakrishnayadav2004@gmail.com

---

**Happy Contributing! 🚀 Let's advance quantum agriculture together!**