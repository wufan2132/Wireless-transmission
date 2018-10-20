from interface import loaddata
from algorithm import dijstra
from network import point
from network.point import point_dict
from simulation import output_generator
from self_cal import Agent
import interface.plotdata

# 导入数据
loaddata.read(r'data/point.xlsx')
output_generator.init(point_dict)
dijstra.init()
Agent.init(point_dict)
for i_episode in range(500):
    # 生成网络输入数据
    output_generator.run(point_dict)

    # 确定网络连接
    dijstra.run()

    # 节点更新
    Agent.run()
    # 显示模块
    # interface.plotdata.draw()
    pass





pass
