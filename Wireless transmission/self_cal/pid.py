class PID():
    def __init__(self, p, i, d, I_limit):
        self.p = p
        self.i = i
        self.d = d
        self.I_limit = I_limit

        self.last_err = 0
        self.sum_err = 0
        self.setPoint = 0
        self.feedback = 0

    def ret_I(self):
        self.sum_err = 0

    def run(self):
        pError = 0
        dError = 0
        Error = self.setPoint - self.feedback
        if Error != 0 and self.i != 0:
            self.sum_err += Error * self.i
            self.sum_err = max(self.sum_err, -self.I_limit)
            self.sum_err = min(self.sum_err, self.I_limit)
        if self.d != 0:
            dError = (Error - self.last_err) * self.d
            self.last_err = Error
        if Error != 0 and self.p != 0:
            pError = Error * self.p
        return pError + self.sum_err + dError
