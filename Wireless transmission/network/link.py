from network import point

link_list = {}


class link(object):
    def __init__(self, loss_factor):
        self.loss_factor = loss_factor
        self.start_node = None
        self.end_node = None
        self.weight = 0
        self.distant = 0
        self.power = 0
        self.start_node_id = None
        self.end_node_id = None

    def connect(self, start, end):
        self.start_node = start
        self.end_node = end
        self.start_node_id = self.start_node.id
        self.end_node_id = self.end_node.id
        self.end_node.input_id = self.start_node.id

        self.power = self.end_node.input / self.loss_factor
        self.start_node.new_output(self.end_node_id, self.power)
        self.cal_weight()
        # 修改上层节点
        self.start_node.change_event()

    def run(self):
        # self.end_node.input = self.start_node.ouput
        output = self.end_node.input / self.loss_factor
        self.start_node.new_output(self.end_node_id, output)
        self.cal_weight()


    def cal_weight(self):
        self.weight = get_weight(self.start_node, self.end_node)
        self.distant = get_distance(self.start_node, self.end_node)

    def change_event(self):
        self.run()
        if self.start_node is None:
            return
        else:
            self.start_node.change_event()

def clear():
    link_list.clear()

def get_distance(start_node, end_node):
    if start_node.id == end_node.id:
        return 0
    distence_weight = (start_node.posX - end_node.posX) * (start_node.posX - end_node.posX) \
                      + (start_node.posY - end_node.posY) * (start_node.posY - end_node.posY)
    return distence_weight


def get_distance_for_id(start_node_id, end_node_id):
    return get_distance(point.point_dict[start_node_id], point.point_dict[end_node_id])


def get_weight(start_node, end_node):
    if start_node.id == end_node.id:
        return 0
    distence_weight = 0.05*((start_node.posX - end_node.posX) * (start_node.posX - end_node.posX) \
                      + (start_node.posY - end_node.posY) * (start_node.posY - end_node.posY))
    power_weight = 110* (
            start_node.sum_output + end_node.input ) \
                   / start_node.max_output
    if power_weight > 100:
        power_weight = 99999999999
    energy_weight = 3000.0 * (start_node.max_energy-start_node.energy) / start_node.max_energy
    # if end_node.name == "移动节点" and start_node.name == "指挥中心":
    #     my_weight = 400
    # else:
    #     my_weight = 0
    weight = distence_weight + power_weight + energy_weight
    return weight


def get_weight_for_id(start_node_id, end_node_id):
    return get_weight(point.point_dict[start_node_id], point.point_dict[end_node_id])


def reget_weight_chain(node_id_list, input):
    pass
