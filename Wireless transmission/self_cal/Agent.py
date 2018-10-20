




class Agent(object):
    def __init__(self, RL_brain=None, PID_brain=None, env=None):
        self.RL_brain = RL_brain
        self.PID_brain = PID_brain
        self.env = env

        # staic message
        self.observation = env.reset()


    def run(self):
        # choose RL or PID?
        pass
        Controller = self.PID_brain
        # get action
        action = Controller.choose_action(self.observation)
        # step
        observation_, reward, done = self.env.step(action)
        # collect information
        pass