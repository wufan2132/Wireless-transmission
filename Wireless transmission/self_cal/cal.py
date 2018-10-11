import self_cal.pid

PID1 = self_cal.pid.PID(100, 0.1, 1, 100)


def cal_input(energy_rate, output):
    PID1.setPoint = 0.8
    PID1.feedback = energy_rate
    input_ = PID1.run() + output
    return input_