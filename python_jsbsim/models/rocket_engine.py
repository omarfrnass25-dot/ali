"""
محرك الصاروخ
مستوحى من FGRocket.cpp في JSBSim
"""

class RocketEngine:
    def __init__(self, isp, max_thrust, fuel_mass):
        self.isp = isp                    # الدفع النوعي (sec)
        self.max_thrust = max_thrust      # أقصى دفع (N)
        self.fuel_mass = fuel_mass        # كتلة الوقود (kg)
        self.throttle = 0.0               # موضع الخانق (0-1)
        
    def calculate(self, dt):
        thrust = self.throttle * self.max_thrust
        fuel_flow = thrust / (self.isp * 9.81)
        self.fuel_mass -= fuel_flow * dt
        return thrust, fuel_flow