import networkx as nx
import matplotlib.pyplot as plt
from network import point, link

color_dict = {"指挥中心": "r",
              "固定节点": "g",
              "移动节点": "y", }
name_dict = {"指挥中心": "A",
             "固定节点": "B",
             "移动节点": "C", }
size_dict = {"指挥中心": 200,
             "固定节点": 150,
             "移动节点": 100, }
def draw():
    G = nx.DiGraph()
    id = [int(p) for p in point.point_dict]
    pos = {p: [point.point_dict[p].posX, point.point_dict[p].posY] for p in point.point_dict}
    color = [color_dict[point.point_dict[p].name] for p in point.point_dict]
    size = [size_dict[point.point_dict[p].name] for p in point.point_dict]
    label = {p:str(p) for p in point.point_dict}
    edge = [(link.link_list[l].start_node_id,l)  for l in link.link_list]
    G.add_nodes_from(id)
    G.add_edges_from(edge)

    nx.draw_networkx_nodes(G, pos, node_color=color, node_size=size)
    nx.draw_networkx_labels(G, pos,label=label)
    nx.draw_networkx_edges(G, pos, width=2, edge_color='k')
    plt.show()

# plt.scatter(x, y, c=c, marker='o')
# plt.show()
# pass
