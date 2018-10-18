"""
Policy Gradient, Reinforcement Learning.
The cart pole example
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
Using:
Tensorflow: 1.0
gym: 0.8.0
"""

import numpy as np
from ReinforceLearning.brain.Policy_Gradient import PolicyGradient
import matplotlib.pyplot as plt
from ReinforceLearning.environment.env import env

DISPLAY_REWARD_THRESHOLD = 400  # renders environment if total episode reward is greater then this threshold
RENDER = False  # rendering wastes time

Myenv = env()

# print(env.action_space)
# print(env.observation_space)
# print(env.observation_space.high)
# print(env.observation_space.low)

RL = PolicyGradient(
    n_actions=Myenv.action_space_num,
    n_features=Myenv.obs_num,
    learning_rate=0.02,
    reward_decay=0.99,
    # output_graph=True,
)
RL.load_model()
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
        action = RL.choose_action(observation)

        observation_, reward, done = Myenv.step(action, Myenv.output_need[step])

        RL.store_transition(observation, action, reward)

        step+=1
        if done:
            ep_rs_sum = sum(RL.ep_rs)

            if 'running_reward' not in globals():
                running_reward = ep_rs_sum
            else:
                running_reward = running_reward * 0.99 + ep_rs_sum * 0.01

            print("episode:", i_episode, "  reward:", int(running_reward), "   run_step:", Myenv.episode)
            vt = RL.clear()
            length = 1000
            sub_axix = np.array(list(range(length)))
            plt.cla()
            plt.title('Result Analysis')
            plt.plot(sub_axix, np.array(input_list[0:length]), color='green', label='input')
            plt.plot(sub_axix, np.array(Myenv.output_need[0:length]), color='red', label='output')
            plt.plot(sub_axix, np.array(energy_list[0:length]), color='blue', label='energy')
            plt.legend()  # 显示图例
            plt.pause(1)

            break
        observation = observation_