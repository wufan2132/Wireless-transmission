from ReinforceLearning.environment.env import env
from ReinforceLearning.brain.lstm_kennel import LSTM

if __name__ == "__main__":
    # maze game
    Myenv = env()
    RL = LSTM(Myenv.action_space_num, Myenv.obs_num,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    step = 0
    for episode in range(3000):
        # initial observation
        observation = Myenv.reset()

        while True:
            # fresh env
            Myenv.render()

            # RL choose action based on observation
            action = RL.choose_action(observation)

            # RL take action and get next observation and reward
            observation_, reward, done = Myenv.step(action, Myenv.output_need[step])

            RL.store_transition(observation, action, reward, observation_)

            if (step > 200) and (step % 5 == 0):
                RL.learn()

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                RL.learn()
                break
            step += 1
            if step == 20000:
                step = 200
