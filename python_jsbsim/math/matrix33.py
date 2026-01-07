import numpy as np

class Matrix33:
    """فئة المصفوفات 3x3 باستخدام NumPy للأداء العالي"""

    def __init__(self, data=None):
        if data is None:
            self.data = np.eye(3, dtype=float)
        elif isinstance(data, np.ndarray) and data.shape == (3, 3):
            self.data = data.copy()
        elif isinstance(data, list) and len(data) == 3 and all(len(row) == 3 for row in data):
            self.data = np.array(data, dtype=float)
        else:
            raise ValueError("يجب أن تكون البيانات مصفوفة 3x3")

    def __add__(self, other):
        if isinstance(other, Matrix33):
            return Matrix33(self.data + other.data)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Matrix33):
            return Matrix33(self.data - other.data)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Matrix33):
            return Matrix33(np.dot(self.data, other.data))
        elif isinstance(other, (int, float)):
            return Matrix33(self.data * other)
        return NotImplemented

    def __rmul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Matrix33(self.data * scalar)
        return NotImplemented

    def transpose(self):
        """النقل"""
        return Matrix33(self.data.T)

    def inverse(self):
        """العكس"""
        return Matrix33(np.linalg.inv(self.data))

    def determinant(self):
        """المصفوفة المحددة"""
        return np.linalg.det(self.data)

    @staticmethod
    def rotation_x(angle):
        """مصفوفة الدوران حول X"""
        c = np.cos(angle)
        s = np.sin(angle)
        return Matrix33([
            [1, 0, 0],
            [0, c, -s],
            [0, s, c]
        ])

    @staticmethod
    def rotation_y(angle):
        """مصفوفة الدوران حول Y"""
        c = np.cos(angle)
        s = np.sin(angle)
        return Matrix33([
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c]
        ])

    @staticmethod
    def rotation_z(angle):
        """مصفوفة الدوران حول Z"""
        c = np.cos(angle)
        s = np.sin(angle)
        return Matrix33([
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1]
        ])

    def __repr__(self):
        return f"Matrix33(\n{self.data}\n)"

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value