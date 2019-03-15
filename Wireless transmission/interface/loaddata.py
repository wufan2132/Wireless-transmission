import csv
from network import point
from network import link


def read(filename):
    workbook = csv.reader(open(filename, 'r'))
    head_row = next(workbook)
    for rows in workbook:
        p = point.point(rows)
        point.point_dict[p.id] = p


def write(filename):
    f = open(filename, 'a', newline="")
    f.seek(0)
    f.truncate()  # 清空文件
    csv_write = csv.writer(f)
    for i, l in enumerate(link.link_list):
        csv_write.writerow([i+1, link.link_list[l].start_node_id+1, link.link_list[l].end_node_id+1])
