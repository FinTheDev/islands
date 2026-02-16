import numpy as np
import math

def perspective(fov, aspect, near, far):
    f = 1.0 / math.tan(fov / 2.0)
    m = np.zeros((4, 4), dtype='float32')
    m[0][0] = f / aspect
    m[1][1] = f
    m[2][2] = (far + near) / (near - far)
    m[2][3] = (2 * far * near) / (near - far)
    m[3][2] = -1.0
    return m

def identity():
    return np.identity(4, dtype='float32')
