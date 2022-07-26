# script version 1.3
from google_sheets import google_sheets_methods
from config import settings

URL_from = settings.URL_info


def get_train_info(carriage_number=None):
    document = google_sheets_methods.GoogleSheets(
        spreadsheet_url_from=URL_from
    )
    worksheet = document.get_worksheet_by_name('Таблица составов')
    head_values = worksheet.row_values(1)
    try:
        searched_train = worksheet.find(carriage_number)
    except Exception as e:
        return f'вагон {carriage_number} не найден в таблице'

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

    title_name = document.get_title_name()
    head_carriage = '№ ГВ'
    tail_carriage = '№ ХВ'
    result_string = f"Ссылка на оригинальную таблицу:\n" \
                    f"<a href='{URL_from}'>{title_name}</a>\n\n" \
                    f"<b>Поиск по значению</b> <i>{carriage_number}</i>\n\n" \
                    f"<b>Информация о составе</b> <i>{result_dict[head_carriage]}" \
                    f"-{result_dict[tail_carriage]}</i>\n\n"

    for key in result_dict:
        result_string += f'<b>{key}</b> : <i>{result_dict[key]}</i>\n'
    return result_string
