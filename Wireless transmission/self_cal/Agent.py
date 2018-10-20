

class Agent(object):
    def __init__(self, rl_brain=None, pid_brain=None, env=None):
        self.RL_brain = rl_brain
        self.PID_brain = pid_brain
        self.env = env

        # staic message
        self.observation = env.reset()

        # Evaluation
        self.Switch_Threshold = -1000
        self.MAX_SIZE = 500
        self.reward_list = []

    def run(self):
        # choose RL or PID?
        controller = self._choose_brain()
        # get action
        action = controller.choose_action(self.observation)
        # step
        self.observation, reward, done = self.env.step(action)
        # collect information
        self._collect_information(reward)
        pass

    def _collect_information(self, reward):
        if len(self.reward_list) >= self.MAX_SIZE:
            self.reward_list.pop(0)
        self.reward_list.append(reward)

    def _choose_brain(self):
        sum_reward = sum(self.reward_list)
        if sum_reward > self.Switch_Threshold:
            return self.RL_brain
        else:
            return self.PID_brain
