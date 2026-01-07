import numpy as np
from .vector3 import Vector3
from .matrix33 import Matrix33

class Quaternion:
    """فئة الـ Quaternion للتوجيه، مستوحاة من FGQuaternion في JSBSim"""

    def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0):
        self.data = np.array([w, x, y, z], dtype=float)

    @property
    def w(self):
        return self.data[0]

    @w.setter
    def w(self, value):
        self.data[0] = value

    @property
    def x(self):
        return self.data[1]

    @x.setter
    def x(self, value):
        self.data[1] = value

    @property
    def y(self):
        return self.data[2]

    @y.setter
    def y(self, value):
        self.data[2] = value

    @property
    def z(self):
        return self.data[3]

    @z.setter
    def z(self, value):
        self.data[3] = value

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            w1, x1, y1, z1 = self.data
            w2, x2, y2, z2 = other.data
            return Quaternion(
                w1*w2 - x1*x2 - y1*y2 - z1*z2,
                w1*x2 + x1*w2 + y1*z2 - z1*y2,
                w1*y2 - x1*z2 + y1*w2 + z1*x2,
                w1*z2 + x1*y2 - y1*x2 + z1*w2
            )
        return NotImplemented

    def conjugate(self):
        """المرافق"""
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inverse(self):
        """العكس"""
        norm_sq = np.dot(self.data, self.data)
        if norm_sq > 0:
            return self.conjugate() * (1.0 / norm_sq)
        return Quaternion()

    def normalize(self):
        """التطبيع"""
        norm = np.linalg.norm(self.data)
        if norm > 0:
            self.data /= norm
        return self

    def normalized(self):
        """إرجاع نسخة طبيعية"""
        norm = np.linalg.norm(self.data)
        if norm > 0:
            return Quaternion(* (self.data / norm))
        return Quaternion()

    def to_euler(self):
        """تحويل إلى زوايا أويلر (Yaw, Pitch, Roll)"""
        w, x, y, z = self.data
        # تجنب gimbal lock
        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = np.arctan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (w * y - z * x)
        if abs(sinp) >= 1:
            pitch = np.copysign(np.pi / 2, sinp)  # gimbal lock
        else:
            pitch = np.arcsin(sinp)

        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = np.arctan2(siny_cosp, cosy_cosp)

        return yaw, pitch, roll

    @staticmethod
    def from_euler(yaw, pitch, roll):
        """إنشاء من زوايا أويلر"""
        cr = np.cos(roll * 0.5)
        sr = np.sin(roll * 0.5)
        cp = np.cos(pitch * 0.5)
        sp = np.sin(pitch * 0.5)
        cy = np.cos(yaw * 0.5)
        sy = np.sin(yaw * 0.5)

        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy

        return Quaternion(w, x, y, z)

    def to_matrix(self):
        """تحويل إلى مصفوفة دوران"""
        w, x, y, z = self.data
        return Matrix33([
            [1 - 2*y*y - 2*z*z, 2*x*y - 2*w*z, 2*x*z + 2*w*y],
            [2*x*y + 2*w*z, 1 - 2*x*x - 2*z*z, 2*y*z - 2*w*x],
            [2*x*z - 2*w*y, 2*y*z + 2*w*x, 1 - 2*x*x - 2*y*y]
        ])

    def derivative(self, omega):
        """حساب مشتقة الـ Quaternion مع omega (Vector3)"""
        if isinstance(omega, Vector3):
            q_omega = Quaternion(0, omega.x, omega.y, omega.z)
            return 0.5 * self * q_omega
        return NotImplemented

    def __repr__(self):
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value