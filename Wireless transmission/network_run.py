from interface import loaddata
from algorithm import dijstra
from network import point
from network.point import point_dict
import interface.plotdata
loaddata.read(r'data/point.xlsx')

dijstra.run()
interface.plotdata.draw()

for p in point_dict:
    point_dict[p].run()

pass
