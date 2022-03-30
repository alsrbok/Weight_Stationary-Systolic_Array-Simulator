from PEarray import *

def main():
    print('Start PE calculation test\n')
    model = PEarray()

    print('Initial psum state of systolic array model')
    model.print_psum_buff()
    print('')

    #Initial state : pe_array_height,width : 2 / throughput_size = 2
    """
    print('Test for pe_array_width=2, pe_array_hegith=2, throughput_size=2\n')
    input_mat1 = np.arange(1,5)
    input_mat1.resize(pe_array_height, throughput_size)

    weight_mat1 = np.arange(1,5)
    weight_mat1.resize(pe_array_width, pe_array_height)

    model.assign_input(input_mat1)
    model.assign_weight(weight_mat1)

    print('Initial state of buffer')
    model.print_input_buff()
    model.print_weight_buff()
    print('')

    model.overall_action()

    print('Result of overall_action')
    model.print_psum_buff()
    print('')
    model.array_initialize()
    """

    # Initial state : pe_array_height,width : 2 / throughput_size = 4
    """
    print('Test for pe_array_width=2, pe_array_hegith=2, throughput_size=4\n')
    input_mat11 = np.arange(1, 9)
    input_mat11.resize(pe_array_height, throughput_size)

    weight_mat1 = np.arange(1, 5)
    weight_mat1.resize(pe_array_height, pe_array_width)

    model.assign_input(input_mat11)
    model.assign_weight(weight_mat1)

    print('Initial state of buffer')
    model.print_input_buff()
    model.print_weight_buff()
    print('')

    model.overall_action()

    print('Result of overall_action')
    model.print_psum_buff()
    print('')
    model.array_initialize()
    """

    # Initial state : pe_array_height = 4 / width : 2 / throughput_size = 2
    """
    print('Test for pe_array_width=2, pe_array_hegith=4, throughput_size=2\n')
    input_mat1 = np.arange(1, 9)
    input_mat1.resize(pe_array_height, throughput_size)

    weight_mat1 = np.arange(1, 9)
    weight_mat1.resize(pe_array_width, pe_array_height)

    model.assign_input(input_mat1)
    model.assign_weight(weight_mat1)

    print('Initial state of buffer')
    model.print_input_buff()
    model.print_weight_buff()
    print('')

    model.overall_action()

    print('Result of overall_action')
    model.print_psum_buff()
    print('')
    model.array_initialize()
    print('Check Initialization')
    model.print_pe_psum()
    model.print_psum_buff()
    model.print_weight_buff()
    model.print_input_buff()
    print('')
    '''
    print('Check for next cycle')
    model.assign_input(input_mat1)
    model.assign_weight(weight_mat1)

    print('Initial state of buffer')
    model.print_input_buff()
    model.print_weight_buff()
    print('')

    model.overall_action()

    print('Result of overall_action')
    model.print_psum_buff()
    print('')
    '''
    """

    # Initial state : pe_array_height = 4 / width : 2 / throughput_size = 8

    print('Test for pe_array_width=4, pe_array_hegith=4, throughput_size=4\n')
    input_mat1 = np.arange(1, 17)
    input_mat1.resize(pe_array_height, throughput_size)

    weight_mat1 = np.arange(1, 17)
    weight_mat1.resize(pe_array_width, pe_array_height)

    model.assign_input(input_mat1)
    model.assign_weight(weight_mat1)

    print('Initial state of buffer')
    model.print_input_buff()
    model.print_weight_buff()
    print('')

    model.overall_action(1)

    print('Result of overall_action')
    model.print_psum_buff()
    print('')
    model.array_initialize_except_psum()
    model.psum_buff_initialize()
    print('Check Initialization')
    model.print_pe_psum()
    model.print_psum_buff()
    model.print_weight_buff()
    model.print_input_buff()
    print('')





if __name__ == '__main__':
    main()