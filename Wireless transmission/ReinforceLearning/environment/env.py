from network.node import node
import math
import numpy as np


class env():
    def __init__(self):
        # 初始化单个节点
        self.node = node(500, 30, 1000)  # max_energy, max_input, max_output
        self.node.set_energy("65%")
        self.node.output[1] = 0
        self.aim_energy_rate = 0.8
        # 初始化输入信息
        self.output_need = [20 + 20 * math.sin(x * 0.031415926) for x in range(1, 20001)] #周期为200, 50
        self.input_list = []
        self.energy_list = []
        self.output_value_list = []
        # 相关环境信息
        self.action_space_num = 3
        self.obs_num = 6
        self.last_reward = 0
        # 其他
        self.last_ob = np.zeros([1, self.obs_num])
        self.episode = 0

    def render(self):
        print("energy:", float(self.node.energy / self.node.max_energy), " input:", self.node.input,
              " output:",self.node.output[1], " reward:", self.last_reward)

    def step(self, action, output_need):
        self.episode += 1
        if action == 0:
            self.node.input += 1
        elif action == 1:
            pass
        elif action == 2:
            self.node.input -= 1
        self.node.set_input(self.node.input)
        self.node.new_output(1, output_need)
        ret, value = self.node.run()
        ob = self.get_obs()
        # reward = -0.1*(self.node.input-output_need)*(self.node.input-output_need)
        if ret == 1: # 正常情况
            self.last_reward = 1-self.node.energy / self.node.max_energy
            done = 0
        elif ret == 0: # 不够了
            self.last_reward = -5.0
            done = 0
        else: # 满了
            self.last_reward = -1.0
            done = 0
        if self.episode > 9999:
            done = 1
        # if self.episode < 200:
        #     self.last_reward = 0
        return ob, self.last_reward, done

    def reset(self):
        self.episode = 0
        self.node.set_energy("85%")
        self.node.set_input(self.output_need[0])
        return self.get_obs()

    def get_obs(self):
        energy_rate = 2.0*self.node.energy / self.node.max_energy -1
        node_input = self.node.input / 40.0 - 20
        node_output = self.node.output[1] / 40.0 - 20
        try:
            if(energy_rate > self.last_energy_rate):
                energy_rate_flag = 1
            else:
                energy_rate_flag = -1
        except:
            energy_rate_flag = 0

        try:
            if (node_input > self.last_node_input):
                node_input_flag = 1
            else:
                node_input_flag = -1
        except:
            node_input_flag = 0

        try:
            if(energy_rate > self.last_node_output):
                node_output_flag = 1
            else:
                node_output_flag = -1
        except:
            node_output_flag = 0

        ob =  np.array([energy_rate, node_input, node_output, energy_rate_flag, node_input_flag, node_output_flag]).astype(np.float32)
        self.last_energy_rate = energy_rate
        self.last_node_input = node_input
        self.last_node_output = node_output
        return ob