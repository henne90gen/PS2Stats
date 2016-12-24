import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('PlanetsideStatsCreator.json', scope)
gc = gspread.authorize(credentials)


def write(data, spreadsheet_name):
    wks = gc.open(spreadsheet_name).sheet1
    data_list = []
    rows = len(data)
    cols = 0
    for data_point in data:
        cols = len(data_point)
        for value in data_point:
            data_list.append(value)

    cell_list = wks.range('A1:' + chr(cols + 64) + str(rows))

    for i in range(len(cell_list)):
        cell_list[i].value = data_list[i]

    wks.update_cells(cell_list)
