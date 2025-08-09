import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import TwoLocal
from qiskit_aer import Aer
from sklearn.preprocessing import StandardScaler
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

class CustomQuantumYieldPredictor:
    """
    Custom Variational Quantum Regressor implementation 
    that avoids problematic qiskit-machine-learning dependencies
    """
    
    def __init__(self, num_features=4, num_qubits=None, shots=1024):
        self.num_features = num_features
        self.num_qubits = num_qubits or max(4, num_features)
        self.shots = shots
        self.scaler = StandardScaler()
        self.parameters = None
        self.backend = Aer.get_backend('aer_simulator')
        
        # Create ansatz circuit
        self.ansatz = TwoLocal(
            self.num_qubits, 
            ['ry', 'rz'], 
            'cz', 
            reps=2, 
            insert_barriers=True
        )
        
        # Number of parameters in the ansatz
        self.num_parameters = self.ansatz.num_parameters
        
        print(f"Initialized Quantum Yield Predictor:")
        print(f"  - Features: {self.num_features}")
        print(f"  - Qubits: {self.num_qubits}")
        print(f"  - Parameters: {self.num_parameters}")
        print(f"  - Shots: {self.shots}")
    
    def _create_feature_map(self, x):
        """Create a simple feature map circuit"""
        qc = QuantumCircuit(self.num_qubits)
        
        # Encode features into rotation angles
        for i in range(min(len(x), self.num_qubits)):
            qc.ry(x[i] * np.pi, i)
        
        return qc
    
    def _create_circuit(self, x, parameters):
        """Create the complete quantum circuit"""
        # Feature map
        feature_map = self._create_feature_map(x)
        
        # Parameterized ansatz
        ansatz_bound = self.ansatz.assign_parameters(parameters)
        
        # Combine circuits
        qc = feature_map.compose(ansatz_bound)
        
        # Add measurements
        qc.measure_all()
        
        return qc
    
    def _execute_circuit(self, circuit):
        """Execute circuit and return expectation value"""
        try:
            # Transpile for backend
            transpiled = transpile(circuit, self.backend)
            
            # Run circuit
            job = self.backend.run(transpiled, shots=self.shots)
            result = job.result()
            counts = result.get_counts()
            
            # Calculate expectation value (simplified)
            total_shots = sum(counts.values())
            expectation = 0.0
            
            for bitstring, count in counts.items():
                # Convert bitstring to integer and normalize
                value = int(bitstring, 2) / (2**self.num_qubits - 1)
                expectation += value * count / total_shots
                
            return expectation
            
        except Exception as e:
            print(f"Circuit execution error: {e}")
            return 0.5  # Default fallback
    
    def _cost_function(self, parameters, X, y):
        """Cost function for optimization"""
        total_cost = 0.0
        
        for i, (x_sample, y_target) in enumerate(zip(X, y)):
            circuit = self._create_circuit(x_sample, parameters)
            prediction = self._execute_circuit(circuit)
            
            # Mean squared error
            cost = (prediction - y_target) ** 2
            total_cost += cost
        
        return total_cost / len(X)
    
    def fit(self, X, y):
        """Train the quantum model"""
        print("Training Quantum Yield Predictor...")
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Normalize targets to [0, 1]
        y_min, y_max = np.min(y), np.max(y)
        self.y_min, self.y_max = y_min, y_max
        y_normalized = (y - y_min) / (y_max - y_min)
        
        # Initialize parameters randomly
        initial_params = np.random.uniform(0, 2*np.pi, self.num_parameters)
        
        # Optimize parameters
        print("Starting optimization...")
        result = minimize(
            self._cost_function,
            initial_params,
            args=(X_scaled, y_normalized),
            method='COBYLA',  # Constraint optimization method
            options={'maxiter': 50, 'disp': True}
        )
        
        self.parameters = result.x
        print(f"Training completed. Final cost: {result.fun:.4f}")
        
        return self
    
    def predict(self, X):
        """Make predictions"""
        if self.parameters is None:
            raise ValueError("Model must be trained first!")
        
        X_scaled = self.scaler.transform(X)
        predictions = []
        
        for x_sample in X_scaled:
            circuit = self._create_circuit(x_sample, self.parameters)
            prediction = self._execute_circuit(circuit)
            
            # Denormalize prediction
            denormalized = prediction * (self.y_max - self.y_min) + self.y_min
            predictions.append(denormalized)
        
        return np.array(predictions)
    
    def score(self, X, y):
        """Calculate R² score"""
        predictions = self.predict(X)
        ss_res = np.sum((y - predictions) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0


# Alias for compatibility with existing code
QuantumYieldPredictor = CustomQuantumYieldPredictor


# Example usage and testing
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    n_samples = 20
    
    # Sample features: temperature, humidity, soil_ph, rainfall
    X = np.random.rand(n_samples, 4)
    X[:, 0] *= 40 + 10  # Temperature: 10-50°C
    X[:, 1] *= 100      # Humidity: 0-100%
    X[:, 2] *= 4 + 4    # pH: 4-8
    X[:, 3] *= 200      # Rainfall: 0-200mm
    
    # Generate synthetic yield data with some correlation
    y = (X[:, 0] * 0.1 + X[:, 1] * 0.05 + X[:, 2] * 2 + X[:, 3] * 0.02 + 
         np.random.normal(0, 2, n_samples))
    
    # Create and train model
    model = QuantumYieldPredictor(num_features=4, shots=512)  # Reduced shots for speed
    model.fit(X, y)
    
    # Make predictions
    predictions = model.predict(X)
    score = model.score(X, y)
    
    print(f"\nModel Performance:")
    print(f"R² Score: {score:.3f}")
    print(f"Mean Absolute Error: {np.mean(np.abs(y - predictions)):.3f}")
    
    # Show some predictions vs actual
    print("\nSample Predictions vs Actual:")
    for i in range(min(5, len(y))):
        print(f"Actual: {y[i]:.2f}, Predicted: {predictions[i]:.2f}")