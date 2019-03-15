from network import node, link
from ReinforceLearning.environment.env import env

# 最大储量 输入功率 输出功率
point_para = {"指挥中心": [99999, 0, 1000],
              "固定节点": [2000, 300, 300],
              "移动节点": [500, 30, 100]}  # [500,30,100]

point_dict = {}


class point(node.node):
    def __init__(self, initlist):
        # initlist 0:序号 1:类型 2:能源储量 3:坐标X 4:坐标Y 5:output 6:input
        self.id = int(initlist[0])
        self.name = initlist[1]
        energy = 0.01 * float(initlist[2]) * point_para[self.name][0]
        self.posX = int(initlist[3])
        self.posY = int(initlist[4])
        output = {}
        if float(initlist[5]) != 0:
            output[0] = float(initlist[5])
        input = float(initlist[6])

        super(point, self).__init__(point_para[self.name][0],
                                    point_para[self.name][1],
                                    point_para[self.name][2])
        self.set_status(energy, input, output)
        self.comfirm_input()

        # 其他属性
        self.input_id = None

    def set_env(self):
        self.env = env(self)

    def change_event(self):
        # self.comfirm_input()
        if link.link_list.get((self.input_id, self.id)) is None:
            return
        else:
            link.link_list[(self.input_id, self.id)].change_event()
            return
