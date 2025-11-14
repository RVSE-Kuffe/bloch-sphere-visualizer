import math
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector, Pauli
from qiskit.visualization.bloch import Bloch
from matplotlib.figure import Figure

class QuantumCalculator:
    def __init__(self):
        self.simulator = Aer.get_backend('statevector_simulator')

    def apply_gate(self, state_vector, gate):
        circuit = QuantumCircuit(1)
        circuit.initialize(state_vector, 0)
        
        if gate == 'X':
            circuit.x(0)
        elif gate == 'Y':
            circuit.y(0)
        elif gate == 'Z':
            circuit.z(0)
        elif gate == 'H':
            circuit.h(0)
        elif gate == 'S':
            circuit.s(0)
        elif gate == 'T':
            circuit.t(0)
        elif gate == 'P':
            circuit.p(math.pi, 0)    

        result = self.simulator.run(circuit).result()
        new_statevector = result.get_statevector(circuit)
        
        return new_statevector.data
    
    def create_bloch_image(self, state_vector):
        sv = Statevector(state_vector)

        pauli_x = Pauli('X')
        pauli_y = Pauli('Y')
        pauli_z = Pauli('Z')

        x = sv.expectation_value(pauli_x).real
        y = sv.expectation_value(pauli_y).real
        z = sv.expectation_value(pauli_z).real

        bloch_vec = [x, y, z]
        bloch_sphere = Bloch()
        bloch_sphere.add_vectors(bloch_vec)
        bloch_sphere.make_sphere() 
        return bloch_sphere.fig