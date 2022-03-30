from constant_variable import *

class Control_Buffer():

    def __init__(self):
        self.RE = [0] * pe_array_height         # Control variable for pe's read_enable
        self.WE = [0] * pe_array_width          # Control variable for pe's write_enable
        self.RE[0] = 1                          # RE's initialize value = [1, 0, 0, 0 ...]
        self.flag  = 0                          # Check for end of pe_array[0][0]'s read_enable

    def update_control(self):
        for j in reversed(range(1, pe_array_width)):                        # Shift WE value
            self.WE[j] = self.WE[j - 1]
        self.WE[0] = self.RE[pe_array_height - 1]

        for i in reversed(range(1, pe_array_height)):                       # Shift RE value
            self.RE[i] = self.RE[i - 1]

        if self.flag < throughput_size:
            self.flag += 1

        if self.flag == throughput_size:         # Choose correct RE[0] value
            self.RE[0] = 0
        else:
            self.RE[0] = 1

    def check_finish(self):
        check = 0
        for j in range(pe_array_width):
            check += self.WE[j]
        for i in range(pe_array_height):
            check += self.RE[i]

        if check != 0:
            return 0        # overall_action is not finished
        else:
            self.flag  = 0  # make control_unit's instance var to initial mode
            self.RE[0] = 1
            return 1        # overall_action is finished