from constant_variable import *
from Control_Buffer import *
from PE import *

import numpy as np

class PEarray():

    def __init__(self):
        self.pe_array = np.full((pe_array_height, pe_array_width), PE())

        #self.pe_array = np.zeros((pe_array_height, pe_array_width))
        for row in range(pe_array_height):
            for col in range(pe_array_width):
                self.pe_array[row, col] = PE()

        self.weight_buffer = np.full((pe_array_width, pe_array_height), 0.0)
        self.input_buffer  = np.full((pe_array_height, throughput_size), 0.0)
        self.psum_buffer   = np.full((pe_array_width, throughput_size), 0.0)
        self.control_unit  = Control_Buffer()

    def array_initialize_except_psum(self):
        for row in range(pe_array_height):
            for col in range(pe_array_width):
                self.pe_array[row, col].make_default()

        for row in range(pe_array_width):
            for col in range(pe_array_height):
                self.weight_buffer[row, col] = 0.0

        for row in range(pe_array_height):
            for col in range(throughput_size):
                self.input_buffer[row, col] = 0.0

    def psum_buff_initialize(self):
        for row in range(pe_array_width):
            for col in range(throughput_size):
                self.psum_buffer[row, col] = 0.0

    # control_unit is initialized in the check_finish() function (located in the last line of overall_action)

    def print_pe_psum(self):                                #For Debugging
        print('pe psum val : ')
        for row in range(pe_array_height):
            for col in range(pe_array_width):
                print(self.pe_array[row, col].psum, end=' ')
            print('')

    def print_input_buff(self):
        print('input buffer : ')
        for row in range(pe_array_height):
            for col in range(throughput_size):
                print(self.input_buffer[row][col], end=' ')
            print('')

    def print_weight_buff(self):
        print('weight buffer : ')
        for row in range(pe_array_width):
            for col in range(pe_array_height):
                print(self.weight_buffer[row][col], end=' ')
            print('')

    def print_psum_buff(self):
        print('psum_buffer : ')
        for row in range(pe_array_width):
            for col in range(throughput_size):
                print(self.psum_buffer[row][col], end = ' ')
            print('')

    def return_psum(self, dram_output, begin_row, begin_col, row_size = pe_array_width, col_size = throughput_size):     # This is used in the Cycle_simulator's function
        for row in range(row_size):
            for col in range(col_size):
                dram_output[begin_row + row, begin_col + col] = self.psum_buffer[row, col]


    def assign_input(self, sram_input):                                                 # Use Before every overall_action
        for row in range(pe_array_height):                                              # SRAM -> input_buffer
            for col in range(throughput_size):
                self.input_buffer[row][col] = sram_input[row][col]


    def assign_weight(self, sram_weight):                         # weight buffer : pe_array_width * pe_array_height
        for row in range(pe_array_width):                                               # SRAM -> weight_buffer
            for col in range(pe_array_height):
                self.weight_buffer[row][col] = sram_weight[row][col]

        for row in range(pe_array_height):                                              # SRAM -> PE's instance weight var
            for col in range(pe_array_width):
                self.pe_array[row, col].feeding_weight(self.weight_buffer[col, row])    # Begin with weight1

    def check_prev_pe_input(self, row, col):                        # For col: 1 ~ (pe_array_width-1)
        if self.pe_array[row, col-1].ready_input == 1:
            self.pe_array[row, col].feeding_input(self.pe_array[row, col-1].input)
            self.pe_array[row, col-1].input_initialize()

    def group_A_action(self, row):
        if row >= 1:
            if self.pe_array[row-1, 0].ready_psum == 1:
                self.pe_array[row, 0].psum = self.pe_array[row-1, 0].psum       # get psum value from upper pe
                self.pe_array[row-1, 0].psum_initialize()                       # initialize upper pe's psum value

        if self.pe_array[row, 0].read_enable == 1:
            self.pe_array[row, 0].feeding_input(self.input_buffer[row, 0])      # get input value

            for j in range(throughput_size-1):                                  # update input_buffer
                self.input_buffer[row, j] = self.input_buffer[row, j+1]
            self.input_buffer[row, throughput_size-1] = 0

            self.pe_array[row, 0].action()                                      # calculate the psum value

    def group_BC_action(self, row, col):
        if row >= 1:
            if self.pe_array[row-1, col].ready_psum == 1:
                self.pe_array[row, col].psum = self.pe_array[row-1, col].psum
                self.pe_array[row-1, col].psum_initialize()

        self.pe_array[row, col].action()

        #self.check_prev_pe_input(row, col)

    def group_D_action(self, row):
        if self.pe_array[row, 0].write_enable == 1:
            buffer = self.psum_buffer[0, 0]
            for j in range(throughput_size-1):
                self.psum_buffer[0, j] = self.psum_buffer[0, j+1]               # Role of Shift register : accumulate psum properly
            self.psum_buffer[0, throughput_size-1] = buffer + self.pe_array[row, 0].psum

        if self.pe_array[row-1, 0].ready_psum == 1:
            self.pe_array[row, 0].psum = self.pe_array[row-1, 0].psum
            self.pe_array[row - 1, 0].psum_initialize()

        if self.pe_array[row, 0].read_enable == 1:
            self.pe_array[row, 0].feeding_input(self.input_buffer[row, 0])

            for j in range(throughput_size-1):
                self.input_buffer[row, j] = self.input_buffer[row, j+1]
            self.input_buffer[row, throughput_size-1] = 0

            self.pe_array[row, 0].action()

    def group_EF_action(self, row, col):
        if self.pe_array[row, col].write_enable == 1:
            buffer = self.psum_buffer[col, 0]
            for j in range(throughput_size-1):
                self.psum_buffer[col, j] = self.psum_buffer[col, j+1]               # Role of Shift register : accumulate psum properly
            self.psum_buffer[col, throughput_size-1] = buffer + self.pe_array[row, col].psum

        if self.pe_array[row - 1, col].ready_psum == 1:
            self.pe_array[row, col].psum = self.pe_array[row - 1, col].psum
            self.pe_array[row - 1, col].psum_initialize()

        self.pe_array[row, col].action()

        #self.check_prev_pe_input(row, col)


    def overall_action(self, test_flag=0):
        while 1:
            for row in range(pe_array_height):                                          # Assign read_enable value of pe
                self.pe_array[row, 0].read_enable = self.control_unit.RE[row]
            for col in range(pe_array_width):
                self.pe_array[pe_array_height - 1, col].write_enable = self.control_unit.WE[col]     # Assign write_enable value of pe

            for row in reversed(range(pe_array_height)):
                for col in reversed(range(pe_array_width)):
                    if col > 0:
                        self.check_prev_pe_input(row, col)

            for row in reversed(range(pe_array_height)):
                for col in range(pe_array_width):
                    if row < pe_array_height-1:
                        if col == 0:
                            self.group_A_action(row)
                        else:
                            self.group_BC_action(row, col)
                    elif row == pe_array_height-1:
                        if col == 0:
                            self.group_D_action(row)
                        else:
                            self.group_EF_action(row, col)
                    else:
                        print('Row indexing of PEarray overall action is wrong')


            if(test_flag == 1) :
                print('It is for debugging')
                self.print_input_buff()
                self.print_weight_buff()
                self.print_pe_psum()
                self.print_psum_buff()
                print('')


            self.control_unit.update_control()                                          # Update RE, WE value of control_unit

            if self.control_unit.check_finish() == 1:
                break
