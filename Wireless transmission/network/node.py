class node(object):
    def __init__(self, max_energy, max_input, max_output):
        self.max_energy = max_energy
        self.max_input = max_input
        self.max_output = max_output
        self.input = 0
        self.output = {}
        self.sum_output = sum(list(self.output.values()))
        self.energy = 0
        self.link = None

    def set_status(self, energy, input, output):
        self.energy = energy
        self.input = input
        self.output = output
        self.sum_output = sum(list(self.output.values()))

    def set_energy(self, energy_Percent):
        percent = 0
        if energy_Percent[-1] == '%':
            percent = 0.01 * int(energy_Percent[0:-1])
        else:
            return
        self.energy = percent * self.max_energy

    def run(self):
        d_energy = self.input - self.sum_output
        if d_energy + self.energy >= self.max_energy:
            self.energy = self.max_energy
            return 2, d_energy + self.energy - self.max_energy
        elif d_energy + self.energy < 0:
            return 0, d_energy + self.energy
        else:
            self.energy += d_energy
        return 1, 0

    def set_input(self, input):
        if input > self.max_input:
            self.input = self.max_input
            return 0
        elif input < 0:
            self.input = 0
            return 0
        else:
            self.input = input
            return 1

    def new_output(self, aim_id, output):
        # 如果没有就新建一个
        if self.output.get(aim_id) is None:
            if self.sum_output + output > self.max_output:
                return 0
            else:
                self.output[aim_id] = output
                self.sum_output = sum(list(self.output.values()))
                return 1
        else:  # 如果有就在原来的基础上改变
            if self.sum_output + output - self.output[aim_id] > self.max_output:
                return 0
            else:
                self.output[aim_id] = output
                self.sum_output = sum(list(self.output.values()))
                return 1

    def clear_link(self):
        self.output = []
        self.sum_output = sum(list(self.output.values()))

    def comfirm_input(self):
        self.input = self.sum_output

    # def set_output(self,output):
    #     self.sum_output = sum(self.output)
    #     if output > self.max_output:
    #         self.output = self.max_output
    #         return 0
    #     elif output < 0:
    #         self.output = 0
    #         return 0
    #     else:
    #         self.output = output
    #         return 1
