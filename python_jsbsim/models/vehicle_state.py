from dataclasses import dataclass

from ..math.vector3 import Vector3
from ..math.quaternion import Quaternion
from ..math.matrix33 import Matrix33

@dataclass
class VehicleState:
    position: Vector3        # الموقع (m)
    velocity: Vector3        # السرعة (m/s)
    orientation: Quaternion  # التوجيه
    angular_rates: Vector3   # السرعات الزاوية (rad/s)
    mass: float             # الكتلة (kg)
    inertia: Matrix33       # عزم القصور الذاتي
    fuel_mass: float = 0.0  # كتلة الوقود (kg)