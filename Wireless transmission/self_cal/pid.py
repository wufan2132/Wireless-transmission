
PID_SETPOINT = 0.8


class PID:
    def __init__(self, p, i, d, i_limit):
        self.p = p
        self.i = i
        self.d = d
        self.I_limit = i_limit

        self.last_err = 0
        self.sum_err = 0
        self.setPoint = 0
        self.feedback = 0

    def ret_I(self):
        self.sum_err = 0

    def run(self):
        perror = 0
        derror = 0
        Error = self.setPoint - self.feedback
        if Error != 0 and self.i != 0:
            self.sum_err += Error * self.i
            self.sum_err = max(self.sum_err, -self.I_limit)
            self.sum_err = min(self.sum_err, self.I_limit)
        if self.d != 0:
            derror = (Error - self.last_err) * self.d
            self.last_err = Error
        if Error != 0 and self.p != 0:
            perror = Error * self.p
        return perror + self.sum_err + derror

    def choose_action(self, obs):
        energy_rate, output = obs[0]/10, obs[2]
        self.setPoint = PID_SETPOINT
        self.feedback = energy_rate
        input_ = self.run() + output
        return input_