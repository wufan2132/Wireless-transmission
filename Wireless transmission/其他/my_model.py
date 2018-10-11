from network.node import node
from network.link import link
node_list = []
link_list = []
for i in range(5):
    n = node(i,1000,300,300)
    n.set_energy('50%')
    node_list.append(n)

node_list[1].set_input(10)
node_list[3].set_input(10)
node_list[4].set_input(20)


l = link(0.5)
l.connect(node_list[2],node_list[3])
link_list.append(l)
l = link(0.5)
l.connect(node_list[2],node_list[4])
link_list.append(l)
l = link(0.5)
l.connect(node_list[0],node_list[1])
link_list.append(l)
l = link(0.5)
l.connect(node_list[0],node_list[2])
link_list.append(l)

for n in node_list:
    n.run()


pass