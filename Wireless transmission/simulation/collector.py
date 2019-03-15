import numpy as np

class collector(object):
    def __init__(self):
        self.sum_output = 0
        self.sum_input = 0
        self.batteryRate = 0
        self.sum_reward = 0
    #  统计一段时间的总能量输出
    def sum_output_start(self):
        self.sum_output = 0

    def sum_output_run(self, point_dict):
        sum_output = 0
        for id in point_dict:
            if point_dict[id].name == '移动节点' and point_dict[id].output.get(0) is not None:
                sum_output += point_dict[id].output[0]
        # self.sum_output += sum_output
        return sum_output

    def sum_output_need_run(self, output_dict):
        sum_output_need = 0
        for id in output_dict:
            sum_output_need += output_dict[id].get()
        return sum_output_need

    #  统计一段时间的总能量输入
    def sum_input_start(self):
        self.sum_input = 0

    def sum_input_run(self, point_dict):
        self.sum_input += point_dict[0].sum_output
        return point_dict[0].sum_output

    #  所有节点电池加权百分比
    def sum_batteryRate_run(self, point_dict):
        sum_energy = 0
        sum_max_energy = 0
        for id in point_dict:
            if point_dict[id].name != '指挥中心':
                sum_energy += point_dict[id].energy
                sum_max_energy += point_dict[id].max_energy
        self.batteryRate = 1.0*sum_energy/sum_max_energy
        return self.batteryRate

    # 统计当前所有节点的reward
    def sum_reward_start(self):
        self.sum_reward = 0

    def sum_reward_run(self, Agent_dict):
        sum_reward = 0
        for id in Agent_dict:
            if Agent_dict[id].env.node.name != '指挥中心':
                sum_reward += Agent_dict[id].reward_list[-1]
        self.sum_reward += sum_reward
        return sum_reward

    def sum_transform_rate(self, link_dict):
        sum_power_loss = 0.
        for id in link_dict:
            rate = link_dict[id].distant
            sum_power_loss += link_dict[id].power * rate







