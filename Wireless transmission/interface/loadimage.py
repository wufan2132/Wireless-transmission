import numpy as np
from numpy import *


def load_image_PIL(filename, isFlatten=False):
    import os
    from PIL import Image
    import numpy as np
    isExit = os.path.isfile(filename)
    if isExit == False:
        print("打开失败!")
    img = Image.open(filename)
    # img.save("d:/mnist/Convert_image_11.jpg")    保存文件
    if isFlatten:
        img_flatten = np.array(np.array(img, dtype=np.uint8).flatten())
        return img_flatten, shape(img_flatten)
    else:
        img_arr = np.array(img, dtype=np.uint8)
        return img_arr, shape(img_arr)

img_arr, shape = load_image_PIL("powerdata.bmp")
img_arr = sum(img_arr,axis=2)
min_list = []
for i in range(20,1076):
    min = 1000
    min_index = 0
    for j in range(100,500):
        if img_arr[j,i]<min:
            min = img_arr[j,i]
            min_index = j
    min_list.append(min_index)
min_list.append(307)
min_list.append(308)
min_list.append(309)
min_list.append(309)
min_list.append(311)
min_list.append(312)
min_list.append(313)
min_list.append(313)
min_list.append(314)
min_list.append(314)
min_list.append(315)
min_list.append(316)
# 总长度1068  44.5
output = []
for i in range(240):
    dt = round(i*1068/240.0)
    output.append(min_list[dt])
output = [(579-x)*5.0/59.0 for x in output]
np.save('imagedata', np.array(output))
pass
# 27 -1点
# 1074 -24点
# x基准 579
# dx = 579-x