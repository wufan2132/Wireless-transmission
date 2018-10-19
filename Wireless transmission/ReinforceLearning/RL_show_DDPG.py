"""
Policy Gradient, Reinforcement Learning.
The cart pole example
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
Using:
Tensorflow: 1.0
gym: 0.8.0
"""

from ReinforceLearning.environment.env_cont import env
from ReinforceLearning.brain.DDPG import DDPG
import matplotlib.pyplot as plt
import numpy as np

RENDER = False  # rendering wastes time
MAX_REWARD = 0
Myenv = env()


# print(env.action_space)
# print(env.observation_space)
# print(env.observation_space.high)
# print(env.observation_space.low)

RL = DDPG(
    a_dim=Myenv.action_space_num,
    s_dim=Myenv.obs_num,
    a_bound=Myenv.action_space_bound,
    memory_capacity=10000,
    batch_size=32,
    lr_a=0.001,
    lr_c=0.002,
    gamma=0.9,
    tau=0.01,
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
    ep_reward = 0
    while True:
        # Myenv.render()

        input_list.append(Myenv.node.input)
        energy_list.append(100*Myenv.node.energy/Myenv.node.max_energy)
        # RL choose action based on observation
        action = RL.choose_action(observation)

        observation_, reward, done = Myenv.step(action, Myenv.output_need[step])
        if step > 200:
            ep_reward += reward
        step+=1
        observation = observation_
        if done:
            print("episode:", i_episode, "  reward:", int(ep_reward), "   run_step:", Myenv.episode)

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