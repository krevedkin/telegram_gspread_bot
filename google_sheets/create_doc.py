# script version 1.2
from google_sheets import google_sheets_methods
from google_sheets import data_collections_methods
from config import settings

URL_from = settings.URL_20
URL_to = settings.URL_to
sheet_name = "Лист1"
sheet_id = 739422900


def create_doc(date_one, date_two, employer_name):
    document = google_sheets_methods.GoogleSheets(

        spreadsheet_url_from=URL_from,
        spreadsheet_url_to=URL_to,
        sheet_name_to=sheet_name

    )
    data_collection = data_collections_methods.DataCollections()

    # Delete all values and borders to create empty doc
    document.delete_all_cells(sheet_id=sheet_id)
    document.delete_borders(range="A11:F1000")

    # Get all worksheets names from doc
    months = document.get_all_sheets_names(reverse=True)
    months = months[1:]  # remove unnecessary worksheet name

    # Get all values from doc
    all_doc_values = document.get_all_doc_values(months)

    # Get first and second dates for searching
    first_date = data_collection.first_date_search(all_doc_values, date_one)
    if first_date is None:
        return None
    last_date = data_collection.last_date_search(all_doc_values, date_two)
    if last_date is None:
        return None

    # renew values to searched values
    all_doc_values = all_doc_values[first_date:last_date + 1]

    # sort values and remove all unnecessary values
    sorting_queue = (4, 1, 2, 5, 6, 8)
    all_doc_values = data_collection.create_sorted_list_of_lists(all_doc_values, sorting_queue)

    # get strings indexes for future cells merge
    # rows_list = data_collection.return_row_index_gen(all_doc_values)

    # create and update doc merge_cells requests
    requests_first_merge = document.make_a_request_body(
        start_row_index=9,
        end_row_index=10,
        start_column_index=0,
        end_column_index=3,
        sheet_id=sheet_id,
        row_index_list=data_collection.generate_row_indexes_collection(all_doc_values, word="Дата")
    )
    requests_second_merge = document.make_a_request_body(
        start_row_index=9,
        end_row_index=10,
        start_column_index=3,
        end_column_index=6,
        sheet_id=sheet_id,
        row_index_list=data_collection.generate_row_indexes_collection(all_doc_values, word="Дата")
    )

    document.batch_update({"requests": requests_first_merge})
    document.batch_update({"requests": requests_second_merge})

    # update doc with new data
    first_range = 11
    last_range = len(all_doc_values) + 10
    result_range = f"A{first_range}:F{last_range}"
    document.update(range=result_range, values=all_doc_values)

    # add borders of the cells
    document.add_borders(result_range)

    # update doc with down head information
    first_range = last_range + 1
    last_range = first_range + 4
    down_head_range = f"A{first_range}:F{last_range}"
    employer_name = employer_name
    engineer_name = ""
    constructor_name = ""
    down_head = [
        ["", "", "", "Согласовано"],
        ["", "", "", "Главный инженер", engineer_name],
        ["", "", "", "Начальник конструкторского отдела", constructor_name],
        ["", "", "", "Сотрудник", employer_name],
    ]
    document.update(range=down_head_range, values=down_head)

    # create top head article, employer name and doc's title name
    head_dates = data_collection.create_head_dates(date_one, date_two)
    head_string = f"в период с {head_dates[0]}г. по {head_dates[1]} г. по выполненным работам"
    title_name = f"Отчет по командировке {employer_name} {head_dates[0]} - {head_dates[1]}"
    document.update("A7", head_string)
    document.update("D9", employer_name)
    document.set_title_name(title_name)

    return document.get_url()


if __name__ == '__main__':
    app = create_doc("10.01.20", "15.01.20", "Уважаемый К.О.")
    print(app)

