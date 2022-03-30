import numpy as np

"""
matrix1 = np.zeros((4, 3, 2))
print(matrix1)

matrix2 = np.zeros((2, 5, 4))
print(matrix2)
print('')
"""

if (32 + 18) / \
        (8 +2) > 9:
    print('bigger than 9')
else:
    print('smaller than 9')
print('')

matrix3 = np.arange(1,49)
print(matrix3)

matrix4 = np.reshape(matrix3, (2, 2, 3, 4))
print(matrix4)
print(matrix4[1, 1, 1, 2])