from ReinforceLearning.environment.env import env
from ReinforceLearning.brain.DeepQNetwork import DeepQNetwork
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    # maze game
    Myenv = env()
    RL = DeepQNetwork(Myenv.action_space_num, Myenv.obs_num,
                      learning_rate=0.3,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=500,
                      memory_size=2000,
                      # output_graph=True
                      )
    step = 0
    plt.figure(figsize=(10, 6), dpi=80)
    plt.ion()
    for episode in range(30000):
        # initial observation
        observation = Myenv.reset()
        input_list = []
        step = 0
        while True:
            # fresh env
            Myenv.render()
            input_list.append(Myenv.node.input)
            # RL choose action based on observation
            action = RL.choose_action(observation)

            # RL take action and get next observation and reward
            observation_, reward, done = Myenv.step(action, Myenv.output_need[step])

            RL.store_transition(observation, action, reward, observation_)

            if step % 5 == 0:
                RL.learn()

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            # if done:
            #     RL.learn()
            #     break
            step += 1
            if step == 20000:
                RL.plot()
                plt.pause(1)
                # sub_axix = np.array(list(range(5000)))
                # plt.cla()
                # plt.title('Result Analysis')
                # plt.plot(sub_axix, np.array(input_list[0:5000]), color='green', label='input')
                # plt.plot(sub_axix, np.array(Myenv.output_need[0:5000]), color='red', label='output')
                # plt.legend()  # 显示图例
                # plt.pause(1)
                break
