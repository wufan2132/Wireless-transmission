from network import point, link


def run():
    link.clear()
    for p_id in point.point_dict:
        start_p = find_min_path(p_id)
        if start_p is not None:
            start_p.change_event()


def init():
    run()
    for id in point.point_dict:
        point.point_dict[id].comfirm_input()
    pass


def find_min_path(p_id):
    if point.point_dict[p_id].name == '指挥中心':
        return
    if point.point_dict[p_id].name == '固定节点':
        l = link.link(1)
        start_p = point.point_dict[0]
        end_p = point.point_dict[p_id]
        l.connect(start_p, end_p)
        if link.link_list.get(p_id) is None:
            link.link_list[p_id] = l
        return start_p
    if point.point_dict[p_id].name == '移动节点':
        min_id = 0
        min_weight = link.get_distance(point.point_dict[0], point.point_dict[p_id])
        for id in point.point_dict:
            if point.point_dict[id].name == '固定节点':
                weight = link.get_distance(point.point_dict[id], point.point_dict[p_id])
                if weight < min_weight:
                    min_weight = weight
                    min_id = id
        l = link.link(0.4)
        start_p = point.point_dict[min_id]
        end_p = point.point_dict[p_id]
        l.connect(start_p, end_p)
        if link.link_list.get(p_id) is None:
            link.link_list[p_id] = l
        return start_p
