import xlrd
from network import point


def read(filename):
    workbook = xlrd.open_workbook(filename)
    table = workbook.sheet_by_index(0)
    rows = table.nrows
    cols = table.ncols
    for i in range(1,rows):
        list = table.row_values(i)
        p = point.point(list)
        point.point_dict[p.id] = p



