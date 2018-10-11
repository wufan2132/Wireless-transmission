from network import node
import self_cal.cal
import interface.plotline
from method import myfunc
node1 = node.node(10000, 30, 1000)  # max_energy, max_input max,_output
node1.set_energy("65%")
output_need = [myfunc.function(x/30) for x in range(1, 1000)]

input_list = []
energy_list = []
output_value_list = []

for op in output_need:
    output_ = op
    node1.new_output(1, output_)
    input_ = self_cal.cal.cal_input(node1.energy / node1.max_energy, output_)
    node1.set_input(input_)
    node1.run()
    print("run...")
    print("input:", input_)
    input_list.append(node1.input)
    print("output:", output_)
    output_value_list.append(node1.output[1])
    print("energy:", node1.energy)
    energy_list.append(node1.energy / node1.max_energy * 100)
    print("")

interface.plotline.draw(input_list, output_need, output_value_list, energy_list)
pass
