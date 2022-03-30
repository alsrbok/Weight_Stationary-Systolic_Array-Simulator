import math

#some needed global variable
data_component_size = 8  # We use 8 bytes float component

#global variable for Conv layer size ( height = row / width = col )
"""
#default value
ifmap_height  = 224
ifmap_width   = 224
ifmap_channel = 3

filter_height = 3
filter_width  = 3

ofmap_height  = 224
ofmap_width   = 224
ofmap_channel = 64

stride        = 1
"""

ifmap_height  = 4
ifmap_width   = 4
ifmap_channel = 3

filter_height = 3
filter_width  = 3

ofmap_height  = 4
ofmap_width   = 4
ofmap_channel = 64

stride        = 1

#global variable for DRAM matrix ( height = row / width = col )
weight_matrix_height = ofmap_channel
weight_matrix_width  = filter_height * filter_width * ifmap_channel

input_matrix_height  = weight_matrix_width
input_matrix_width   = ofmap_height * ofmap_width

output_matrix_height = weight_matrix_height
output_matrix_width  = input_matrix_width

#SRAM size (Design Specification)
SRAM_size = 80000                           #80KB

#Design parameter of PE array
pe_array_height = 4                         # M value , YOU SHOULD CONSIDER EDGE PART OF WEIGHT MATRIX WIDTH(27 % 4 = 3)
pe_array_width  = 16                         # N value ( wanna be divisor of ofmap_channel(64))
"""
throughput_size = 256                       # hyper parameter based on HW specification
"""
throughput_size = 4

input_buffer_size  = pe_array_height * throughput_size * data_component_size              #8KB for 4*256*8
psum_buffer_size   = pe_array_width  * throughput_size * data_component_size              #4KB for 2*256*8
weight_buffer_size = pe_array_width  * pe_array_height * data_component_size              #64B for 2*4*8

#constant value used in Cycle_Simulator
"""
dram_to_sram_bw = 10000                                                                    # 10KB/cycle
"""
dram_to_sram_bw = 32

required_tile_set_amount = math.ceil(input_matrix_height / pe_array_height)                # 7 : how many tile set is required for one psum block
usable_SRAM_size = SRAM_size - input_buffer_size - weight_buffer_size - psum_buffer_size   # 67.648KB for 80000-8192-64-4096
enabled_tile_set_amount = int(usable_SRAM_size / (weight_buffer_size + input_buffer_size)) # 8 for int(67648/(8192+64)) : how many tile set can be used at once

#For SRAM Case 1,2,3
SRAM_input_size = required_tile_set_amount * pe_array_height * throughput_size * data_component_size # 57.344KB for 7*4*256*8
remain_SRAM_size = usable_SRAM_size - SRAM_input_size                                                # 10.304KB for 67648 - 57344
enabled_num_of_psum_group = int(remain_SRAM_size / (pe_array_width * pe_array_height * required_tile_set_amount))  # 184 for 10304 / (2*4*7)

enabled_sram_weight_channel_int_num = math.floor(enabled_num_of_psum_group / pe_array_width) # enabled channel num of sram_weight

sram_weight_channel_num = weight_matrix_height / pe_array_width # It can be integer or real number -> should be control in logic :32
sram_weight_channel_int_num = math.ceil(sram_weight_channel_num) # required total channel num of sram_weight :32


#SRAM_weight_size_1 = pe_array_width * pe_array_height * required_tile_set_amount * enable_num_of_psum_group

