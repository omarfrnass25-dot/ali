"""
حساب التسارعات
مستوحى من FGAccelerations في JSBSim
"""

from ..math.vector3 import Vector3

def calculate_accelerations(state, forces, moments, gravity):
    total_forces = forces + gravity * state.mass
    linear_accel = total_forces / state.mass
    angular_accel = state.inertia.inverse() @ (moments - state.angular_rates.cross(state.inertia @ state.angular_rates))
    return linear_accel, angular_accel