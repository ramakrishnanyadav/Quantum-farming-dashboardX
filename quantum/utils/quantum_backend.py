from qiskit_aer import Aer
from qiskit import transpile
from config import settings

def get_quantum_backend(backend_type, shots=1024):
    """
    Configures and returns a quantum backend instance.
    Note: QuantumInstance is deprecated in Qiskit 1.0+
    """
    print(f"Configuring backend: {backend_type} with {shots} shots.")
    
    # Remove the extra characters from the radio button label
    clean_backend_type = backend_type.replace('🖥️', '').replace('🔬', '').strip()

    if clean_backend_type == 'Simulator':
        backend = Aer.get_backend('aer_simulator')
        print("✅ Using Aer Simulator")
        
    elif clean_backend_type == 'Fake Device':
        try:
            # Try different import paths for fake backends
            backend = None
            
            # Method 1: Try qiskit-ibm-runtime fake provider
            try:
                from qiskit_ibm_runtime.fake_provider import FakeManila
                backend = FakeManila()
                print("✅ Using FakeManila from qiskit_ibm_runtime")
            except ImportError:
                pass
            
            # Method 2: Try original fake provider
            if backend is None:
                try:
                    from qiskit.providers.fake_provider import FakeManila
                    backend = FakeManila()
                    print("✅ Using FakeManila from qiskit.providers")
                except ImportError:
                    pass
            
            # Method 3: Try FakeManilaV2
            if backend is None:
                try:
                    from qiskit.providers.fake_provider import FakeManilaV2
                    backend = FakeManilaV2()
                    print("✅ Using FakeManilaV2")
                except ImportError:
                    pass
            
            # Method 4: Try other fake backends
            if backend is None:
                try:
                    from qiskit.providers.fake_provider import FakeVigo
                    backend = FakeVigo()
                    print("✅ Using FakeVigo as fallback")
                except ImportError:
                    pass
            
            # Final fallback to simulator
            if backend is None:
                print("⚠️ No fake backends available, using simulator")
                backend = Aer.get_backend('aer_simulator')
                
        except Exception as e:
            print(f"⚠️ Error loading fake backend: {e}")
            print("Falling back to simulator")
            backend = Aer.get_backend('aer_simulator')
            
    elif clean_backend_type == 'Real Quantum':
        if settings.IBM_QUANTUM_TOKEN and "your_" not in settings.IBM_QUANTUM_TOKEN:
            try:
                # Try new IBM Quantum Runtime approach
                from qiskit_ibm_runtime import QiskitRuntimeService
                
                # Save account if not already saved
                try:
                    QiskitRuntimeService.save_account(
                        token=settings.IBM_QUANTUM_TOKEN,
                        overwrite=True
                    )
                except Exception as save_error:
                    print(f"Account save error (might already exist): {save_error}")
                
                # Get service and backend
                service = QiskitRuntimeService()
                backend = service.least_busy(operational=True, simulator=False)
                print(f"✅ Connected to IBM Quantum backend: {backend.name}")
                
            except ImportError:
                print("⚠️ qiskit_ibm_runtime not available, trying legacy approach")
                try:
                    from qiskit import IBMQ
                    IBMQ.save_account(settings.IBM_QUANTUM_TOKEN, overwrite=True)
                    IBMQ.load_account()
                    provider = IBMQ.get_provider('ibm-q/open/main')
                    backend = provider.get_backend('ibmq_qasm_simulator')
                    print("✅ Connected to IBM Quantum (legacy).")
                except Exception as e:
                    print(f"⚠️ Error connecting to IBM Quantum: {e}")
                    backend = Aer.get_backend('aer_simulator')
            except Exception as e:
                print(f"⚠️ Error connecting to IBM Quantum: {e}")
                backend = Aer.get_backend('aer_simulator')
        else:
            print("⚠️ Real Quantum backend selected, but no valid token found. Using simulator.")
            backend = Aer.get_backend('aer_simulator')
    else:
        print(f"⚠️ Unknown backend '{backend_type}'. Defaulting to simulator.")
        backend = Aer.get_backend('aer_simulator')

    # Return a dictionary with backend info instead of deprecated QuantumInstance
    return {
        'backend': backend,
        'shots': shots,
        'optimization_level': 1,
        'seed_simulator': 42
    }

def run_circuit(circuit, backend_config):
    """
    Helper function to run a circuit with the backend configuration.
    This replaces the deprecated QuantumInstance.execute() method.
    """
    backend = backend_config['backend']
    shots = backend_config['shots']
    
    # Transpile the circuit for the backend
    transpiled_circuit = transpile(circuit, backend)
    
    # Run the circuit
    job = backend.run(transpiled_circuit, shots=shots)
    result = job.result()
    
    return result