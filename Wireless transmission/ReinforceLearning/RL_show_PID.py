"""
Policy Gradient, Reinforcement Learning.
The cart pole example
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
Using:
Tensorflow: 1.0
gym: 0.8.0
"""

import numpy as np
from self_cal.pid import PID
import matplotlib.pyplot as plt
from ReinforceLearning.environment.env import env

DISPLAY_REWARD_THRESHOLD = 400  # renders environment if total episode reward is greater then this threshold
RENDER = False  # rendering wastes time

Myenv = env()

# print(env.action_space)
# print(env.observation_space)
# print(env.observation_space.high)
# print(env.observation_space.low)

pid_brain = PID(100, 0.1, 1, 100)
plt.figure(figsize=(10, 6), dpi=80)
plt.ion()
for i_episode in range(3000):

    observation = Myenv.reset()
    input_list = []
    energy_list = []
    step = 0

    while True:
        # Myenv.render()

        input_list.append(Myenv.node.input)
        energy_list.append(100*Myenv.node.energy/Myenv.node.max_energy)
        # RL choose action based on observation
        action = pid_brain.choose_action(observation)

        observation_, reward, done = Myenv.step(action, Myenv.output_need[step])

        step+=1
        if done:
            length = 1000
            start = 3000
            sub_axix = np.array(list(range(length)))
            plt.cla()
            plt.title('Result Analysis')
            plt.plot(sub_axix, np.array(input_list[start:start+length]), color='green', label='input')
            plt.plot(sub_axix, np.array(Myenv.output_need[start:start+length]), color='red', label='output')
            plt.plot(sub_axix, np.array(energy_list[start:start+length]), color='blue', label='energy')
            plt.legend()  # 显示图例
            plt.pause(1)

            break
        observation = observation_