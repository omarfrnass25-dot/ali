"""
نموذج الجاذبية WGS84
مستوحى من FGInertial في JSBSim
"""

from ..math.vector3 import Vector3

class Gravity:
    """نموذج الجاذبية"""

    def __init__(self):
        self.mu = 3.986004418e14  # WGS84 gravitational parameter (m³/s²)
        self.R = 6378137  # WGS84 equatorial radius (m)

    def get_gravity_vector(self, position):
        """حساب متجه الجاذبية عند الموقع (Vector3)"""
        r = position.magnitude()
        if r > 0:
            g_magnitude = self.mu / r**2
            # اتجاه نحو مركز الأرض (سالب لأن position من المركز)
            return -g_magnitude * (position / r)
        # fallback للارتفاع 0
        return Vector3(0, 0, -9.80665)

    def get_gravity_magnitude(self, position):
        """قوة الجاذبية (m/s²)"""
        r = position.magnitude()
        if r > 0:
            return self.mu / r**2
        return 9.80665

# مثال الاستخدام
if __name__ == "__main__":
    gravity = Gravity()
    pos = Vector3(0, 0, 6371000)  # سطح الأرض
    g_vec = gravity.get_gravity_vector(pos)
    print(f"متجه الجاذبية: {g_vec}")
    print(f"قوة الجاذبية: {gravity.get_gravity_magnitude(pos)} m/s²")