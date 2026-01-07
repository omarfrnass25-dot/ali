"""
تكامل معادلات الحركة 6DOF
مستوحى من FGPropagate في JSBSim
"""

from .vehicle_state import VehicleState
from .integrators import Integrator
from ..math.quaternion import Quaternion

class Propagate:
    def __init__(self, dt):
        self.dt = dt
        self.integrator = Integrator()

    def step(self, state, linear_accel, angular_accel):
        # تكامل السرعة الخطية
        state.velocity = self.integrator.euler(lambda v: linear_accel, state.velocity, self.dt)

        # تكامل الموقع
        state.position = self.integrator.euler(lambda p: state.velocity, state.position, self.dt)

        # تكامل السرعات الزاوية
        state.angular_rates = self.integrator.euler(lambda w: angular_accel, state.angular_rates, self.dt)

        # تكامل التوجيه
        q_dot = state.orientation.derivative(state.angular_rates)
        state.orientation = self.integrator.euler(lambda q: q_dot, state.orientation, self.dt)
        state.orientation.normalize()

        return state