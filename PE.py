class PE():

    # What is the size of input, weight, psum.... numpy matrix? array? float? => element of matrix : float
    def __init__(self):
        self.input   = 0                                            # val of current used input
        self.weight0 = 0                                            # register
        self.weight1 = 0                                            # register
        self.psum    = 0                                            # psum register

        #control signal ( 0: false, 1:true )
        self.ready_input   = 0                                      # 1: can send input value to next pe
        self.ready_psum    = 0                                      # 1: psum calculation is done, can send to next pe
        self.ready_weight  = 0                                      # 1: wegith assign for 1 cycle is finished
        self.select_weight = 0                                      # 0: use weight0 / 1: use weight1

        #scheduler logic
        self.read_enable   = 0                                      # For first column pe / 1: Read data from input_buffer
        self.write_enable  = 0                                      # For last row of pe  / 1: Send data to psum buffer

    def feeding_weight(self, weight_input):                         # Use double buffering / only when ready_psum = 1
        if self.select_weight == 0:
            self.weight1 = weight_input                             # Buffering weight on weight1 which will be used next
            self.select_weight = 1                                  # change for next cycle
        else:
            self.weight0 = weight_input
            self.select_weight = 0

        self.ready_weight = 1

    def feeding_input(self, data_in):                               # data_in : input_buffer / prev pe send this val (based on scheduler)
        self.input = data_in
        self.ready_input = 1

    def action(self):                                               # Calculate the psum
        if self.ready_input == 1 and self.ready_weight ==1:         # Available only when pe has input_val & weight_val
            if self.select_weight == 0:
                self.psum += self.input * self.weight0
            else:
                self.psum += self.input * self.weight1
            self.ready_psum = 1


    def psum_initialize(self):                                       # Use after send psum val to next pe or psum_beffer
        self.psum        = 0
        self.ready_psum  = 0

    def input_initialize(self):                                     # Use after next pe take out the input value
        self.input       = 0
        self.ready_input = 0

    def make_default(self):                                         # Use after the whole throughput calculated
        self.input   = 0
        self.weight0 = 0
        self.weight1 = 0
        self.psum    = 0

        self.ready_input   = 0
        self.ready_psum    = 0
        self.ready_weight  = 0
        self.select_weight = 0

        self.read_enable   = 0
        self.write_enable  = 0
