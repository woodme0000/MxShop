# -*- coding: utf-8 -*-
import xlrd


class Xls_Handle(object):
    """
    处理excel文件
    """
    def __init__(self, xlsfile=None):
        self.xlsfile = xlsfile

    def get_book(self, file):
        """获取excel的book对象"""
        book = xlrd.open_workbook(file)
        return book

    def get_sheet_by_index(self, book, index=0):
        """通过制定索引获取sheet名字,默认取第一个"""
        sheet = book.sheet_name()[index]
        return sheet

    def get_sheet_by_name(self, book, sheet_name):
        """通过sheet名字来获取,如果知道sheet名字就可以直接制定"""
        pass

    def read_xls(self, file, sheet_name):
        book = self.get_book(file)
        sheet = book.sheet_by_name(sheet_name)
        # 取出行数和列数
        row_nums = sheet.nrows
        col_nums = sheet.ncols
        # 获取第一行的数据列表
        row_data = sheet.row_values(0)

        for row_index in range(row_nums):
            print(sheet.row_values(row_index))
        print("我打印完了")

        # 获取第一列的数据列表，返回对象是一个值列表
        col_data = sheet.col_values(0)

        # 通过cell的位置坐标获得指定cell的值
        cell_value = sheet.cell(0,0)

if __name__ == "__main__":

    file = '/usr/local/src/MxShop/数据模板.xls'

    xls = Xls_Handle()

    xls.read_xls(file, 'sheet0')
