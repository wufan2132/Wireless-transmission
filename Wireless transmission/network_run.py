from interface import loaddata
from algorithm import dijstra
from network import point
from network.point import point_dict
from simulation import Random_generated
from self_cal.cal import *
import interface.plotdata

# 导入数据
loaddata.read(r'data/point.xlsx')
Random_generated.output_init(point_dict)

for i_episode in range(500):
    # 确定网络输入数据
    Random_generated.output_run(point_dict)
    # 确定网络连接
    dijstra.run()

    # 节点更新
    for id in point_dict:
        cal_point(point_dict[id])
    # 显示模块
    # interface.plotdata.draw()
    pass





pass
