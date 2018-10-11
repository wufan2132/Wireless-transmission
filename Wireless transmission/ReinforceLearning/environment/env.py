from network.node import node
import math
import numpy as np


class env():
    def __init__(self):
        # 初始化单个节点
        self.node = node(10000, 30, 1000)  # max_energy, max_input max,_output
        self.node.set_energy("65%")
        self.node.output[1] = 0
        self.aim_energy_rate = 0.8
        # 初始化输入信息
        self.output_need = [10 + 10 * math.sin(x * 0.031415926) for x in range(1, 20001)]
        self.input_list = []
        self.energy_list = []
        self.output_value_list = []
        # 相关环境信息
        self.action_space_num = 3
        self.obs_num = 6
        # 其他
        self.last_ob = np.zeros([1, self.obs_num])

    def render(self):
        print("energy:", float(self.node.energy / self.node.max_energy), " input:", self.node.input, " output:",
              self.node.output[1])

    def step(self, action, output_need):
        if action == 0:
            self.node.input += 1
        elif action == 1:
            pass
        elif action == 2:
            self.node.input -= 1
        self.node.set_input(self.node.input)
        self.node.new_output(1, output_need)
        ret, value = self.node.run()
        energy_rate = self.node.energy / self.node.max_energy
        _ob = np.array([energy_rate, self.node.input, self.node.output[1]]).astype(np.float32)
        ob = np.append(_ob, self.last_ob)
        self.last_ob = _ob

        reward = -0.1*(self.node.input-output_need)*(self.node.input-output_need)
        done = 1
        # if ret == 1:
        #     reward = 0.001*(1-energy_rate)
        #     done = 0
        # elif ret == 0:
        #     reward = value
        #     done = 1
        # else:
        #     reward = -0.1*value
        #     done = 1
        return ob, reward, done

    def reset(self):
        self.node.set_energy("65%")
        energy_rate = self.node.energy / self.node.max_energy
        _ob = np.array([energy_rate, self.node.input, self.node.output[1]]).astype(np.float32)
        self.last_ob = _ob
        ob = np.append(_ob, _ob)
        return ob

    # def step(self, action, output_need):
    #     if action == 0:
    #         self.node.input += 1
    #     elif action == 1:
    #         pass
    #     elif action ==2:
    #         self.node.input -= 1
    #     self.node.set_input(self.node.input)
    #     self.node.new_output(1, output_need)
    #     ret = self.node.run()
    #     energy_rate = self.node.energy/self.node.max_energy
    #     ob = np.array([energy_rate, self.aim_energy_rate, self.node.output[1]]).astype(np.float32)
    #     if ret == 1:
    #         reward = 100 - energy_rate * 100
    #         done = 0
    #     else:
    #         reward = -10000
    #         done = 1
    #     info = 0
    #     return ob, reward, done
