from Cycle_Simulator import *

def main():
    print('Start the Convolution Computation by matrix multiplication\n')

    a = np.arange(1, weight_matrix_height * weight_matrix_width + 1)
    weight_matrix = a.reshape(weight_matrix_height, weight_matrix_width)
    b = np.arange(1, input_matrix_height * input_matrix_width + 1)
    input_matrix = b.reshape(input_matrix_height, input_matrix_width)
    """
    weight_matrix = np.full( (weight_matrix_height, weight_matrix_width), 1.0 )
    input_matrix  =np.full( (input_matrix_height, input_matrix_width), 1.0 )
    """

    print('Weight Matrix : \n')
    print(weight_matrix)
    print('')
    print('Input Matrix : \n')
    print(input_matrix)
    print('')

    simulator = Cycle_Simulator()

    simulator.assign_input_matrix(input_matrix)
    simulator.assign_weight_matrix(weight_matrix)

    simulator.output_matrix_caculator()

    print('Output Matrix : \n')
    simulator.print_output_matrix()
    print('')
    simulator.print_dram_access_cycle()

if __name__ == '__main__':
    main()