from PEarray import *

class Cycle_Simulator():

    def __init__(self):
        #Cycle counter
        self.dram_to_sram_cycle = 0
        self.sram_to_dram_cycle = 0

        #For Debugging
        self.computed_output_block_row = 0              # which block in output matrix is computed in 'this' cycle
        self.computed_output_block_col = 0

        self.model = PEarray()

        #DRAM Component
        self.weight_matrix = np.zeros((weight_matrix_height, weight_matrix_width))
        self.input_matrix  = np.zeros((input_matrix_height, input_matrix_width))
        self.output_matrix = np.zeros((output_matrix_height, output_matrix_width))
        self.case_indicator = 0

        #SRAM Component
        if enabled_tile_set_amount > required_tile_set_amount:
            self.SRAM_input = np.zeros((required_tile_set_amount, pe_array_height, throughput_size))

            if enabled_sram_weight_channel_int_num > sram_weight_channel_int_num:
                self.case_indicator = 1      #Case 1 : Every input and weight for first column box of psum are stored in SRAM
                self.SRAM_weight = np.zeros((sram_weight_channel_int_num, required_tile_set_amount,
                                             pe_array_width, pe_array_height))

            else:
                self.case_indicator =2       #Case 2 :Every input and some of weight for first column box of psum are stored in SRAM
                self.SRAM_weight = np.zeros((enabled_sram_weight_channel_int_num, required_tile_set_amount,
                                             pe_array_width, pe_array_height))

        else:
            self.case_indicator = 3          #Case 3 : some of input and weight for first box of psum are stored in SRAM
            self.SRAM_input = np.zeros((enabled_tile_set_amount, pe_array_height, throughput_size))
            self.SRAM_weight = np.zeros((enabled_tile_set_amount, pe_array_width, pe_array_height))

    def assign_weight_matrix(self, conv_weight_matrix):         # assign Conv Layer's weight matrix in to cycle simulator
        for row in range(weight_matrix_height):
            for col in range(weight_matrix_width):
                self.weight_matrix[row, col] = conv_weight_matrix[row, col]

    def assign_input_matrix(self, conv_input_matrix):           # assign Conv Layer's input matrix in to cycle simulator
        for row in range(input_matrix_height):
            for col in range(input_matrix_width):
                self.input_matrix[row, col] = conv_input_matrix[row, col]

    def print_output_matrix(self):
        for row in range(output_matrix_height):
            print('{:02d}'.format(row), " : ", end='')
            for col in range(output_matrix_width):
                print('{:04.2f}'.format(self.output_matrix[row, col]), end=' ')
            print('')

    def print_dram_access_cycle(self):
        print("dram_to_sram_cycle : ", self.dram_to_sram_cycle)
        print("sram_to_dram_cycle : ", self.sram_to_dram_cycle)
        print('')

    def input_dram_to_sram(self, begin_row, begin_col ,row_size, col_size, depth):
        for row in range(row_size):
            for col in range(col_size):
                self.SRAM_input[depth, row, col] = self.input_matrix[begin_row + row, begin_col + col]

    def weight_dram_to_sram(self, begin_row, begin_col, row_size, col_size, depth, channel = -1):
        for row in range(row_size):
            for col in range(col_size):
                if channel == -1:
                    self.SRAM_weight[depth, row, col] = self.weight_matrix[begin_row + row, begin_col + col]
                else:
                    self.SRAM_weight[channel, depth, row, col] = self.weight_matrix[begin_row + row, begin_col + col]

    def output_matrix_caculator(self):
        if self.case_indicator == 1:
            print("You have a nice SRAM")

            # SRAM_input initialize
            for depth in range(required_tile_set_amount - 1):  # For edge of tile use '-1'
                self.input_dram_to_sram(pe_array_height * depth, 0, pe_array_height, throughput_size, depth)
                """
                for row in range(pe_array_height):
                    for col in range(throughput_size):
                        self.SRAM_input[depth, row, col] = self.input_matrix[row + pe_array_height * depth, col]
                """
            # Assign the bottom edge of input tile correctly
            start_point = pe_array_height * (required_tile_set_amount - 1)
            self.input_dram_to_sram(start_point, 0, input_matrix_height - start_point, throughput_size,
                                    (required_tile_set_amount - 1))
            #print(self.SRAM_input)
            #print('')

            #SRAM_weight initialize
            if math.ceil(sram_weight_channel_num) == sram_weight_channel_num:  # pe_array_width is a factor of weight_matrix_height
                for channel in range(sram_weight_channel_int_num):
                    for depth in range(required_tile_set_amount - 1):  # For edge of tile use '-1'
                        self.weight_dram_to_sram(pe_array_width * channel, pe_array_height * depth,
                                                 pe_array_width, pe_array_height, depth, channel)
                        """
                        for row in range(pe_array_width):
                            for col in range(pe_array_height):
                                self.SRAM_weight[channel, depth, row, col] = \
                                    self.weight_matrix[row + pe_array_width * channel, col + pe_array_height * depth]
                        """
                    #Assign the right edge of weight tile correctly
                    start_point = pe_array_height * (required_tile_set_amount - 1)  # 4 * 6 = 24
                    self.weight_dram_to_sram(pe_array_width * channel, start_point, pe_array_width,
                                             weight_matrix_width - start_point, (required_tile_set_amount - 1), channel)
                #print(self.SRAM_weight)
                #print('')

            else:
                for channel in range(sram_weight_channel_int_num - 1): # For bottom edge of tile
                    for depth in range(required_tile_set_amount - 1):  # For right edge of tile
                        self.weight_dram_to_sram(pe_array_width * channel, pe_array_height * depth,
                                                 pe_array_width, pe_array_height, depth, channel)
                    #Assign the right edge of weight tile correctly
                    start_point = pe_array_height * (required_tile_set_amount - 1)  # 4 * 6 = 24
                    self.weight_dram_to_sram(pe_array_width * channel, start_point, pe_array_width,
                                             weight_matrix_width - start_point, (required_tile_set_amount - 1), channel)

                # Assign the bottom edge of weight tile correctly
                start_point_row = pe_array_width * (sram_weight_channel_int_num - 1)
                for depth in range(required_tile_set_amount - 1):
                    self.weight_dram_to_sram(start_point_row, pe_array_height * depth, weight_matrix_height - start_point_row,
                                             pe_array_width, depth, sram_weight_channel_int_num - 1)

                # Assign the bottom and right edge of weight tile
                start_point_col = pe_array_height * (required_tile_set_amount - 1)
                self.weight_dram_to_sram(start_point_row, start_point_col, weight_matrix_height - start_point_row,
                                         weight_matrix_width - start_point_col, (required_tile_set_amount - 1),
                                         sram_weight_channel_int_num - 1)
                #print(self.SRAM_weight)
                #print('')

            # dram_to_sram cycle update for initialization
            self.dram_to_sram_cycle += math.ceil(data_component_size * (weight_matrix_height * weight_matrix_width + \
                                                 input_matrix_height * throughput_size) / dram_to_sram_bw)

            #Overall cycle for each SRAM state
            for cycle in range(int(input_matrix_width / throughput_size)):
                # Loop of "assign PEarray's weight, input buffer -> overall_action(take off psum) -> initialize -> load new SRAM state"
                for channel in range(sram_weight_channel_int_num):
                    #print("PE array will calculate for (", channel, ",", cycle, ") box of output_matrix")
                    for depth in range(required_tile_set_amount): # edge of depth is already concerned and psum do not effected by edge(add 0)
                        # assign PEarray's weight, input buffer
                        self.model.assign_weight(self.SRAM_weight[channel, depth])
                        self.model.assign_input(self.SRAM_input[depth])
                        # overall action for one tile
                        if cycle == 0:
                            self.model.overall_action()
                        else:
                            self.model.overall_action()

                        # initialize the pearray for next iteration
                        self.model.array_initialize_except_psum()

                    # transfer psum from psum_buffer(SRAM) to DRAM for every 1 channel
                    if math.ceil(sram_weight_channel_num) == sram_weight_channel_num:    # pe_array_width is a factor of weight_matrix_height
                        self.model.return_psum(self.output_matrix, pe_array_width * channel, throughput_size * cycle)
                        self.sram_to_dram_cycle += math.ceil(data_component_size * pe_array_width * throughput_size / dram_to_sram_bw)

                    else:
                        if channel < sram_weight_channel_int_num - 1:
                            self.model.return_psum(self.output_matrix, pe_array_width * channel,
                                                   throughput_size * cycle)
                            self.sram_to_dram_cycle += math.ceil(data_component_size * \
                                                                pe_array_width * throughput_size / dram_to_sram_bw)

                        else:
                            start_channel = (sram_weight_channel_int_num - 1)
                            self.model.return_psum(self.output_matrix, pe_array_width * start_channel,
                                                   throughput_size * cycle, output_matrix_height - pe_array_width * start_channel )
                            self.sram_to_dram_cycle += math.ceil(data_component_size * throughput_size * \
                                                                 (output_matrix_height - pe_array_width * start_channel) / dram_to_sram_bw)

                    self.model.psum_buff_initialize()


                # load new input_matrix to sram_input (except for the last iteration) for 1 cycle
                if (cycle + 1) < input_matrix_width / throughput_size:
                    for depth2 in range(required_tile_set_amount - 1):  # For edge of tile use '-1'
                        self.input_dram_to_sram(pe_array_height * depth2, throughput_size * (cycle + 1),
                                                pe_array_height, throughput_size, depth2)

                        start_point = pe_array_height * (required_tile_set_amount - 1)
                        self.input_dram_to_sram(start_point, throughput_size * (cycle + 1), input_matrix_height - start_point,
                                                throughput_size, (required_tile_set_amount - 1))
                    # dram_to_sram cycle update for input SRAM update
                    self.dram_to_sram_cycle += math.ceil(data_component_size * input_matrix_height * throughput_size / dram_to_sram_bw)

        elif self.case_indicator == 2:
            print("You have a medium size of SRAM")

        elif self.case_indicator == 3:
            print("You have a tiny size of SRAM. Upgrade your device.")

        else:
            print("Something goes wrong with the case_indicator variable")