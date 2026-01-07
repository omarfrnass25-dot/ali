import pytest
from python_jsbsim.math.vector3 import Vector3

def test_vector3_add():
    v1 = Vector3(1, 2, 3)
    v2 = Vector3(4, 5, 6)
    result = v1 + v2
    assert result.x == 5
    assert result.y == 7
    assert result.z == 9