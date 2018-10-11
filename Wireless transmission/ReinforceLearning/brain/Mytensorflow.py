import tensorflow as tf
import numpy as np


class Mytensorflow():
    def __init__(self):
        self.model_list = []
        self.x_input = None
        self.y_input = None
        self.output = None
        self.loss = None
        self.train_step = None
        self.init = None
        self.sess = None
        # para
        self.training_times = 1000
        self.alpha = 0.1

    def set_para(self, times=1000, alpha=0.1):
        self.training_times = times
        self.alpha = alpha

    def make_model(self, numlist):
        """
        比如 list = [2,10,10,1]
        input
        """
        if (len(numlist) < 2):
            return None
            # input_layer
        input_size = numlist[0]
        out_size = numlist[-1]
        with tf.name_scope("inputs"):
            self.x_input = tf.placeholder(tf.float32, [None, input_size], name="x_input")
            self.y_input = tf.placeholder(tf.float32, [None, out_size], name="y_input")
            self.model_list.append(self.x_input)
        # mid_layer
        for i in range(1, len(numlist) - 1):
            with tf.name_scope("mid_layer"+str(i)):
                mid_layer = self.__add_layer(self.model_list[-1], numlist[i - 1], numlist[i], act_fun=tf.nn.sigmoid)
                self.model_list.append(mid_layer)
        # output_layer
        with tf.name_scope("output"):
            self.output = self.__add_layer(self.model_list[-1], numlist[-2], numlist[-1], act_fun=tf.nn.sigmoid)
            self.model_list.append(self.output)

        # loss
        with tf.name_scope("loss"):
            self.loss = tf.reduce_mean(tf.reduce_sum(tf.square(self.y_input - self.output)))
        # train
        self.train_step = tf.train.GradientDescentOptimizer(self.alpha).minimize(self.loss)
        # var_init
        self.init = tf.global_variables_initializer()
        return self.model_list

    def train(self, x_data, y_data):
        self.sess = tf.Session()
        writer = tf.summary.FileWriter("logs/", self.sess.graph)
        self.sess.run(self.init)
        for i in range(self.training_times):
            self.sess.run(self.train_step, feed_dict={self.x_input: x_data, self.y_input: y_data})
            print("loss:", self.sess.run(self.loss, feed_dict={self.x_input: x_data, self.y_input: y_data}))
        prediction_value = self.sess.run(self.output, feed_dict={self.x_input: x_data})
        return prediction_value

    def predict(self, x_data):
        prediction_value = self.sess.run(self.output, feed_dict={self.x_input: x_data})
        return prediction_value



    def __add_layer(self, input_x, in_size, out_size, act_fun=None):
        with tf.name_scope("weights"):
            Weight = tf.Variable(tf.random_normal([in_size, out_size]))
        with tf.name_scope("biases"):
            biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
        with tf.name_scope("Wx_plus_b"):
            Wx_plus_b = tf.matmul(input_x, Weight) + biases
        if act_fun is None:
            outputs = Wx_plus_b
        else:
            outputs = act_fun(Wx_plus_b)
        return outputs

