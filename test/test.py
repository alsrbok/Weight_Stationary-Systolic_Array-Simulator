import numpy as np
from PE import *
from constant_variable import *
class Cell():
    def __init__(self):
        self.value = 1
        self.attribute1 = False
        self.attribute2 = False

mat = np.full((3, 3), Cell())

print(type(mat))
print(type(mat[2, 2]))
print(mat[2,1].value)
print('')

pearray = np.full((pe_array_height,pe_array_width), PE())
print(type(pearray))
print(type(pearray[1, 1]))
print(pearray[1,0].write_enable)
print('')
