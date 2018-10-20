from ReinforceLearning.environment.env import env
from ReinforceLearning.brain.Policy_Gradient import PolicyGradient
from self_cal.pid import PID
Agent_dict = {}


def init(point_dict):
    rl_brain = PolicyGradient(
        n_actions=env.action_space_num,
        n_features=env.obs_num,
        learning_rate=0.02,
        reward_decay=0.99,
        # output_graph=True,
    )
    rl_brain.load_model(path='ReinforceLearning/saved_model/policy_gradient.ckpt')
    # 所有节点共用一个RL，PID控制器是独立的
    for id in point_dict:
        if id != 0:
            pid_brain = PID(100, 0.1, 1, 100)
            e = env(point_dict[id])
            a = Agent(rl_brain, pid_brain, e)
            Agent_dict[id] = a


def run():
    for id in Agent_dict:
        Agent_dict[id].run()


class Agent(object):
    def __init__(self, rl_brain=None, pid_brain=None, env=None):
        self.RL_brain = rl_brain
        self.PID_brain = pid_brain
        self.env = env

        # staic message
        self.observation = env.get_obs()

        # Evaluation
        self.Switch_Threshold = -1000
        self.MAX_SIZE = 500
        self.reward_list = []
        self.reward_sum = sum(self.reward_list)

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
            self.reward_sum -= self.reward_list.pop(0)
        self.reward_list.append(reward)
        self.reward_sum += reward

    def _choose_brain(self):
        if self.reward_sum > self.Switch_Threshold:
            return self.RL_brain
        else:
            return self.PID_brain
