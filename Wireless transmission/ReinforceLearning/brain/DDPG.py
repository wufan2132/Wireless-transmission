import tensorflow as tf
import numpy as np



class DDPG(object):
    def __init__(self, a_dim, s_dim, a_bound,
                 lr_a=0.001, lr_c=0.002, gamma=0.9, tau=0.01,
                 memory_capacity=10000, batch_size=32):
        self.memory_capacity = memory_capacity
        self.batch_size = batch_size
        self.lr_a = lr_a
        self.lr_c = lr_c
        self.gamma = gamma
        self.tau = tau

        self.memory = np.zeros((self.memory_capacity, s_dim * 2 + a_dim + 1), dtype=np.float32)
        self.pointer = 0


        self.a_dim, self.s_dim, self.a_bound = a_dim, s_dim, a_bound,
        self.S = tf.placeholder(tf.float32, [None, s_dim], 's')
        self.S_ = tf.placeholder(tf.float32, [None, s_dim], 's_')
        self.R = tf.placeholder(tf.float32, [None, 1], 'r')

        self.a = self._build_a(self.S, )
        q = self._build_c(self.S, self.a, )
        a_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Actor')
        c_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Critic')
        ema = tf.train.ExponentialMovingAverage(decay=1 - tau)  # soft replacement

        def ema_getter(getter, name, *args, **kwargs):
            return ema.average(getter(name, *args, **kwargs))

        target_update = [ema.apply(a_params), ema.apply(c_params)]  # soft update operation
        a_ = self._build_a(self.S_, reuse=True, custom_getter=ema_getter)  # replaced target parameters
        q_ = self._build_c(self.S_, a_, reuse=True, custom_getter=ema_getter)

        a_loss = - tf.reduce_mean(q)  # maximize the q
        self.atrain = tf.train.AdamOptimizer(self.lr_a).minimize(a_loss, var_list=a_params)

        with tf.control_dependencies(target_update):  # soft replacement happened at here
            q_target = self.R + self.gamma * q_
            td_error = tf.losses.mean_squared_error(labels=q_target, predictions=q)
            self.ctrain = tf.train.AdamOptimizer(self.lr_c).minimize(td_error, var_list=c_params)

        self.saver = tf.train.Saver(max_to_keep=1)
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def choose_action(self, s):
        return self.sess.run(self.a, {self.S: s[np.newaxis, :]})[0]

    def add_noisy(self,action, scale=30):
        return np.clip(np.random.normal(action, scale), -self.a_bound, self.a_bound)  # add randomness to action selection for exploration

    def learn(self):
        indices = np.random.choice(self.memory_capacity, size=self.batch_size)
        bt = self.memory[indices, :]
        bs = bt[:, :self.s_dim]
        ba = bt[:, self.s_dim: self.s_dim + self.a_dim]
        br = bt[:, -self.s_dim - 1: -self.s_dim]
        bs_ = bt[:, -self.s_dim:]

        self.sess.run(self.atrain, {self.S: bs})
        self.sess.run(self.ctrain, {self.S: bs, self.a: ba, self.R: br, self.S_: bs_})

    def store_transition(self, s, a, r, s_):
        transition = np.hstack((s, a, [r], s_))
        index = self.pointer % self.memory_capacity  # replace the old memory with new memory
        self.memory[index, :] = transition
        self.pointer += 1



    def _build_a(self, s, reuse=None, custom_getter=None):
        trainable = True if reuse is None else False
        with tf.variable_scope('Actor', reuse=reuse, custom_getter=custom_getter):
            net = tf.layers.dense(s, 30, activation=tf.nn.relu, name='l1', trainable=trainable)
            a = tf.layers.dense(net, self.a_dim, activation=tf.nn.tanh, name='a', trainable=trainable)
            return tf.multiply(a, self.a_bound, name='scaled_a')

    def _build_c(self, s, a, reuse=None, custom_getter=None):
        trainable = True if reuse is None else False
        with tf.variable_scope('Critic', reuse=reuse, custom_getter=custom_getter):
            n_l1 = 30
            w1_s = tf.get_variable('w1_s', [self.s_dim, n_l1], trainable=trainable)
            w1_a = tf.get_variable('w1_a', [self.a_dim, n_l1], trainable=trainable)
            b1 = tf.get_variable('b1', [1, n_l1], trainable=trainable)
            net = tf.nn.relu(tf.matmul(s, w1_s) + tf.matmul(a, w1_a) + b1)
            return tf.layers.dense(net, 1, trainable=trainable)  # Q(s,a)


    def save_model(self,path='saved_model/ddpg.ckpt'):
        self.saver.save(self.sess, path)

    def load_model(self,path='saved_model/ddpg.ckpt'):
        self.saver.restore(self.sess, path)

    def show_para(self):
        self.sess.run(tf.global_variables_initializer())
        fc1_kernel = self.sess.run(tf.global_variables('fc1/kernel')[0])
        print(fc1_kernel)
        fc1_bias = self.sess.run(tf.global_variables('fc1/bias')[0])
        print(fc1_bias)

        fc2_kernel = self.sess.run(tf.global_variables('fc2/kernel')[0])
        print(fc2_kernel)
        fc2_bias = self.sess.run(tf.global_variables('fc2/bias')[0])
        print(fc2_bias)

        # fc3_kernel = self.sess.run(tf.global_variables('fc3/kernel')[0])
        # print(fc3_kernel)
        # fc3_bias = self.sess.run(tf.global_variables('fc3/bias')[0])
        # print(fc3_bias)
        #
        # fc4_kernel = self.sess.run(tf.global_variables('fc4/kernel')[0])
        # print(fc4_kernel)
        # fc4_bias = self.sess.run(tf.global_variables('fc4/bias')[0])
        # print(fc4_bias)

        pass