from network import point, link

aim_list = {} # 待连接的节点

shortest_list = {}
make_list = {}

def run():
    link.clear()
    point_dict = point.point_dict.copy()
    sorted(point_dict, key=lambda p: point_dict[p].input, reverse=True)
    for p_id in point.point_dict:
        path_message = find_min_path(p_id)
        link_path(path_message)
        point.point_dict[p_id].change_event()
        pass

def find_min_path(aim_id):
    # edgedict = {}
    # # 初始化权值
    # for start_id in point.point_dict:
    #     for end_id in point.point_dict:
    #         edgedict[(start_id, end_id)] = link.get_weight(point.point_dict[start_id], point.point_dict[end_id])

    # 生成对应的初始化弧
    for p_id in point.point_dict:
        if p_id != 0:
            make_list[p_id] = [link.get_weight_for_id(0, p_id), [0, p_id]]
        else:
            make_list[p_id] = [link.get_weight_for_id(0, p_id), [0]]

    # 找最小路径
    while {} != make_list:
        # 取最小值的弧确认
        min_id = min(make_list, key=make_list.get)
        # 选择最小的确定出队
        shortest_list[min_id] = make_list.pop(min_id)
        # 更新其他的节点
        for m_id in make_list:
            new_path = shortest_list[min_id][0] + link.get_weight_for_id(min_id, m_id)
            # 如果小就加进去
            if new_path < make_list[m_id][0]:
                make_list[m_id][0] = new_path
                make_list[m_id][1] = shortest_list[min_id][1].copy()
                make_list[m_id][1].append(m_id)
    return shortest_list[aim_id]

def link_path(path_message):
    for i in range(len(path_message[1])-1):
        if i == len(path_message[1])-1:
            break
        else:
            l = link.link(1)
            start_p = point.point_dict[path_message[1][i]]
            end_p = point.point_dict[path_message[1][i + 1]]
            l.connect(start_p, end_p)
            if link.link_list.get(path_message[1][i + 1]) is None:
                link.link_list[path_message[1][i + 1]] = l
            # else:
            #     link.link_list[(path_message[1][i], path_message[1][i + 1])] = l


def init():
    run()
    for id in point.point_dict:
        point.point_dict[id].comfirm_input()
    pass


# def init():
#     # edgedict = {}
#     # # 初始化权值
#     # for start_id in point.point_dict:
#     #     for end_id in point.point_dict:
#     #         edgedict[(start_id, end_id)] = link.get_weight(point.point_dict[start_id], point.point_dict[end_id])
#
#     # 生成对应的初始化弧
#     for p_id in point.point_dict:
#         if p_id != 0:
#             make_list[p_id] = [link.get_distance_for_id(0, p_id), [0, p_id]]
#         else:
#             make_list[p_id] = [link.get_distance_for_id(0, p_id), [0]]
#
#     # 找最小路径
#     while {} != make_list:
#         # 取最小值的弧确认
#         min_id = min(make_list, key=make_list.get)
#         # 选择最小的确定出队
#         shortest_list[min_id] = make_list.pop(min_id)
#         # 更新其他的节点
#         for m_id in make_list:
#             new_path = shortest_list[min_id][0] + link.get_distance_for_id(min_id, m_id)
#             # 如果小就加进去
#             if new_path < make_list[m_id][0]:
#                 make_list[m_id][0] = new_path
#                 make_list[m_id][1] = shortest_list[min_id][1].copy()
#                 make_list[m_id][1].append(m_id)

    # # 生成link
    # for pt in shortest_list:
    #     for i in range(len(shortest_list[pt][1])-1):
    #         if i == len(shortest_list[pt][1])-1:
    #             break
    #         else:
    #             l = link.link(1)
    #             start_p = point.point_dict[shortest_list[pt][1][i]]
    #             end_p = point.point_dict[shortest_list[pt][1][i+1]]
    #             l.connect(start_p, end_p)
    #             if link.link_list.get((shortest_list[pt][1][i], shortest_list[pt][1][i + 1])) is None:
    #                 link.link_list[(shortest_list[pt][1][i], shortest_list[pt][1][i+1])] = l
    #             # else:
    #             #     link.link_list[(shortest_list[pt][1][i], shortest_list[pt][1][i + 1])] = l
    #
    #
    #
def Iter():
    pass

def setlink():
    pass












