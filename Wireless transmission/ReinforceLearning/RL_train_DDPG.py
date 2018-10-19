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
scale = 2
for i_episode in range(500):

    observation = Myenv.reset()
    input_list = []
    ep_reward = 0
    step = 0

    while True:
        # Myenv.render()
        input_list.append(Myenv.node.input)
        # RL choose action based on observation
        action = RL.choose_action(observation)
        action = RL.add_noisy(action, scale)

        observation_, reward, done = Myenv.step(action, Myenv.output_need[step])
        if step > 200:
            RL.store_transition(observation, action, reward, observation_)
        # 更新标志
        step += 1
        ep_reward += reward
        observation = observation_

        if done:
            RL.learn()
            scale *= 0.995
            print("episode:", i_episode, "  reward:", int(ep_reward), "   run_step:", Myenv.episode,
                  "   Explore: %.2f" % scale)
            if ep_reward > MAX_REWARD:
                MAX_REWARD = ep_reward
                RL.save_model()
            break

if MAX_REWARD == 0:
    RL.save_model()
