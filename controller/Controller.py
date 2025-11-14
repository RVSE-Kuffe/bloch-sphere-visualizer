import numpy as np

class Controller:
    def __init__(self, quantum_calculator):
        self.quantum_calculator = quantum_calculator
        self.state_vector = [1, 0]
        pass

    #TODO    
    def set_base_bloch_sphere(self, alpha_real, alpha_imagine, beta_real, beta_imagine):
        try:
            alpha = float(alpha_real) + 1j * float(alpha_imagine)
            beta = float(beta_real) + 1j * float(beta_imagine)
            
            vec = [alpha, beta]
            
            norm = np.linalg.norm(vec)
            
            if np.isclose(norm, 0):
                return False

            self.state_vector = vec / norm
            return True

        except (ValueError, TypeError):
            return False
    
    def apply_gate(self, gate):
        self.state_vector = self.quantum_calculator.apply_gate(self.state_vector, gate)
    
    def get_sphere_image(self):
        return self.quantum_calculator.create_bloch_image(self.state_vector)