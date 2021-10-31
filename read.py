import xlrd
def readData(path):
    book = xlrd.open_workbook(path)
    sheet = book.sheets()[0]
    info = sheet.row_values(1)
    return info
