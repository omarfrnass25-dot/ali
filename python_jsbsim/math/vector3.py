import numpy as np

class Vector3:
    """فئة المتجهات ثلاثية الأبعاد باستخدام NumPy للأداء العالي"""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.data = np.array([x, y, z], dtype=float)

    @property
    def x(self):
        return self.data[0]

    @x.setter
    def x(self, value):
        self.data[0] = value

    @property
    def y(self):
        return self.data[1]

    @y.setter
    def y(self, value):
        self.data[1] = value

    @property
    def z(self):
        return self.data[2]

    @z.setter
    def z(self, value):
        self.data[2] = value

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(*(self.data + other.data))
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(*(self.data - other.data))
        return NotImplemented

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector3(*(self.data * scalar))
        return NotImplemented

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector3(*(self.data / scalar))
        return NotImplemented

    def dot(self, other):
        """ضرب نقطي"""
        if isinstance(other, Vector3):
            return np.dot(self.data, other.data)
        return NotImplemented

    def cross(self, other):
        """ضرب تقاطعي"""
        if isinstance(other, Vector3):
            return Vector3(*np.cross(self.data, other.data))
        return NotImplemented

    def magnitude(self):
        """الطول"""
        return np.linalg.norm(self.data)

    def normalize(self):
        """التطبيع"""
        mag = self.magnitude()
        if mag > 0:
            self.data /= mag
        return self

    def normalized(self):
        """إرجاع نسخة طبيعية"""
        mag = self.magnitude()
        if mag > 0:
            return Vector3(*(self.data / mag))
        return Vector3()

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value