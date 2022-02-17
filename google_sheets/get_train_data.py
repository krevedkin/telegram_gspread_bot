# script version 1.0
from google_sheets import google_sheets_methods
from config import settings

URL_from = settings.URL_TEST


def get_train_info(train_number):
    document = google_sheets_methods.GoogleSheets(
        spreadsheet_url_from=URL_from
    )
    worksheet = document.get_worksheet_by_name('Список депо')
    head_values = worksheet.row_values(1)

    try:
        searched_train = worksheet.find(train_number)
    except Exception as e:
        return f'состав {train_number} не найден в таблице'

    searched_values = worksheet.row_values(searched_train.row)

    for i, item in enumerate(searched_values):
        if item == '' or item == ' ':
            searched_values[i] = 'нет данных'

    if len(searched_values) < len(head_values):
        for _ in range(len(head_values) - len(searched_values)):
            searched_values.append('нет данных')

    result_dict = {}
    for i, item in enumerate(head_values):
        result_dict[item] = searched_values[i]

    result_string = f"Информация о составе {train_number}\n\n"
    for key in result_dict:
        result_string += f'<b>{key}</b> : <i>{result_dict[key]}</i>\n'
    return result_string
