import numpy as np
import math

class mingyu():

    def __init__(self, num):
        self.i = 0
        self.num = num

        if num > 5:
            self.i = 3
            array = np.arange(1, 16)
            self.minarray = array.reshape((3, 5))

        else:
            self.i = 2
            array = np.arange(1, 11)
            self.minarray = array.reshape((2, 5))

    def print_i(self):
        print(self.i, '\n')

    def print_array(self):
        print(self.minarray)
        print('')

if __name__ == '__main__':
    min_obj1 = mingyu(7)
    min_obj1.print_i()
    min_obj1.print_array()

    min_obj2 = mingyu(3)
    min_obj2.print_i()
    min_obj2.print_array()