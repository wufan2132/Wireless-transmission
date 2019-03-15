from ReinforceLearning.environment.env import env
from ReinforceLearning.brain.Policy_Gradient import PolicyGradient
from self_cal.pid import PID
Agent_dict = {}
import copy

def init(point_dict):
    rl_brain = PolicyGradient(
        n_actions=env.action_space_num,
        n_features=env.obs_num,
        learning_rate=0.02,
        reward_decay=0.99,
        # output_graph=True,
    )
    rl_brain.load_model(path='ReinforceLearning/saved_model/PG - 1/policy_gradient.ckpt')
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
        self.virtual_env = None
        self.controller = None
        # staic message
        self.observation = env.get_obs()

        # Evaluation
        self.Switch_Threshold = -0
        self.MAX_SIZE = 500
        self.reward_list = []
        self.reward_sum = sum(self.reward_list)
        self.reward_rl_list = []
        self.reward_rl_sum = sum(self.reward_rl_list)

    def run(self):
        # choose RL or PID?
        self.controller = self._choose_brain()
        # get action
        action = self.controller.choose_action(self.observation)
        action_for_rl = self.RL_brain.choose_action(self.observation)
        # step
        self.virtual_env = copy.deepcopy(self.env)
        _, reward_rl, _ = self.virtual_env.step(action_for_rl)

        self.observation, reward, _ = self.env.step(action)
        # collect information
        self._collect_rl_information(reward_rl)
        self._collect_information(reward)
        pass


    def _collect_information(self, reward):
        if len(self.reward_list) >= self.MAX_SIZE:
            self.reward_sum -= self.reward_list.pop(0)
        self.reward_list.append(reward)
        self.reward_sum += reward


    def _collect_rl_information(self, reward):
        if len(self.reward_rl_list) >= self.MAX_SIZE:
            self.reward_rl_sum -= self.reward_rl_list.pop(0)
        self.reward_rl_list.append(reward)
        self.reward_rl_sum += reward

    def _choose_brain(self):
        if self.reward_rl_sum > self.Switch_Threshold:
            return self.RL_brain
        else:
            return self.PID_brain
