import math
import random
d = {0: 1, 1: 2, 2: 1, 3: 0}
def function(x):
    y = 20+20*math.sin(x)
    return y

def smooth(list):
    for i in range(4, len(list)-4):
        list[i] = (list[i-2] + list[i+2] + list[i-1] + list[i+1] + list[i])/5

# y = math.sin(x)*x
#  y = x*x + x + 10*x*math.sin(x)
# int(x)%2
# y = random.random()

