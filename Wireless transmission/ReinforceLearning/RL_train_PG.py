"""
Policy Gradient, Reinforcement Learning.
The cart pole example
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
Using:
Tensorflow: 1.0
gym: 0.8.0
"""

import gym
from ReinforceLearning.brain.Policy_Gradient import PolicyGradient
import matplotlib.pyplot as plt
from ReinforceLearning.environment.env import env


RENDER = False  # rendering wastes time
MAX_REWARD = 0
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
for i_episode in range(200):

    observation = Myenv.reset()
    input_list = []
    step = 0
    while True:
        # Myenv.render()
        input_list.append(Myenv.node.input)
        # RL choose action based on observation
        action = RL.choose_action(observation)

        observation_, reward, done = Myenv.step(action, Myenv.output_need[step])
        if step > 200:
            RL.store_transition(observation, action, reward)
        step += 1
        if done:
            ep_rs_sum = sum(RL.ep_rs)

            if 'running_reward' not in globals():
                running_reward = ep_rs_sum
            else:
                running_reward = running_reward * 0.9 + ep_rs_sum * 0.1

            print("episode:", i_episode, "  reward:", int(running_reward), "   run_step:", Myenv.episode)

            vt = RL.learn()

            if i_episode == 0:
                plt.plot(vt)    # plot the episode vt
                plt.xlabel('episode steps')
                plt.ylabel('normalized state-action value')
                plt.show()

            if running_reward > MAX_REWARD:
                MAX_REWARD = running_reward
                RL.save_model()
            break
        observation = observation_
if MAX_REWARD == 0:
    RL.save_model()
