import math
import numpy as np

output_dict = {}


def output_init(point_dict):
    for id in point_dict:
        if point_dict[id].name == '移动节点':
            # 为所有末端节点绑定一个输出源
            output_dict[id] = output_generator()
            output = output_dict[id].run()
            point_dict[id].new_output(-1, output)

def output_run(point_dict):
    for id in output_dict:
        output = output_dict[id].run()
        point_dict[id].new_output(-1, output)

class output_generator(object):
    def __init__(self, scale=None, bias=None,
                 period=None, phase=None,
                 max_iter=20000):
        # 随机生成
        if scale is None:
            scale = np.random.randint(0, 25)
        if bias is None:
            bias = np.random.randint(scale, max(scale, 25))
        if period is None:
            period = np.random.randint(50, 400)
        if phase is None:
            phase = np.random.randint(0, period)
        self.output = [bias + scale * math.sin(x * 6.2831852 * 2 / period + 6.2831852 * 2 / phase) for x in
                       range(0, max_iter)]
        self.iter = 0
        self.max_iter = max_iter

    def run(self):
        output = self.output[self.iter]
        self.iter += 1
        if self.iter >= self.max_iter:
            self.iter = 0
        return output


class pos_generator(object):
    pass