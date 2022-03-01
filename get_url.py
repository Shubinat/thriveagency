import openpyxl

fname = 'parse.xlsx'
links = []
def get_url():
    wb = openpyxl.load_workbook(fname)
    sheet = wb.get_sheet_by_name('Web Design Industrija')
    row = '37'
    print(row)
    for rowOfCellObjects in sheet['A1':'A'+row]:
        for cellObj1 in rowOfCellObjects:
            links.append(cellObj1.value)
    return links
