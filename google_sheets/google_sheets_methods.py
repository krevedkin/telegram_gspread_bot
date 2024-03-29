# script version 1.5
import gspread
from google_sheets.data_collections_methods import DataCollections
from config import path_to_creds


class GoogleSheets:
    """Class for work with Google Spreadsheets API"""

    def __init__(self, spreadsheet_url_from: str,
                 spreadsheet_url_to: str = None,
                 sheet_name_to: str = None,
                 ) -> None:
        """Authentication in google"""
        self.spreadsheet_url_from = spreadsheet_url_from
        self.client = gspread.service_account(filename=path_to_creds)
        self.spreadsheet_from = self.client.open_by_url(self.spreadsheet_url_from)
        if spreadsheet_url_to and sheet_name_to is not None:
            self.spreadsheet_url_to = spreadsheet_url_to
            self.sheet_name_to = sheet_name_to
            self.spreadsheet_to = self.client.open_by_url(self.spreadsheet_url_to)

    def update(self, range: str, values: str or list) -> None:
        """Method for update spreadsheet objects"""
        self.spreadsheet_to.worksheet(self.sheet_name_to).update(range, values)

    def batch_update(self, request: dict) -> None:
        """Method for batch update spreadsheet objects using dictionaries of JSON data"""
        self.spreadsheet_to.batch_update(request)

    def set_title_name(self, title_name: str) -> None:
        """Sets name of the spreadsheet"""
        request = {
            "requests": [
                {
                    "updateSpreadsheetProperties": {
                        "properties": {
                            "title": title_name
                        },
                        "fields": "title"
                    }
                }
            ]
        }

        self.spreadsheet_to.batch_update(request)

    def get_url(self) -> str:
        """Return spreadsheet URL"""
        return self.spreadsheet_to.url

    def add_request(self, start_row_index: int,
                    end_row_index: int,
                    start_column_index: int,
                    end_column_index: int,
                    sheet_id: int) -> dict:
        """Creates a single JSON request for merge cells"""
        additional_request = {
            "mergeCells": {
                "mergeType": "MERGE_ROWS",
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": start_row_index,
                    "endRowIndex": end_row_index,
                    "startColumnIndex": start_column_index,
                    "endColumnIndex": end_column_index,
                },
            }
        }
        return additional_request

    def make_a_request_body(
            self,
            start_row_index: int,
            end_row_index: int,
            start_column_index: int,
            end_column_index: int,
            sheet_id: int,
            row_index_list: list,
            merge_type: str = "MERGE_ROWS") -> list:
        """Creates JSON request body for merge cells batch update """
        requests_list = []
        if merge_type == "MERGE_ROWS":
            for item in row_index_list:
                requests_list.append(
                    self.add_request(
                        start_row_index + item,
                        end_row_index + item,
                        start_column_index,
                        end_column_index,
                        sheet_id,
                    )
                )
        return requests_list

    def add_borders(self, range: str) -> None:
        """Creates borders of the cells by JSON format"""
        self.spreadsheet_to.worksheet(self.sheet_name_to).format(
            range,
            {
                "borders": {
                    "top": {"style": "SOLID"},
                    "bottom": {"style": "SOLID"},
                    "left": {"style": "SOLID"},
                    "right": {"style": "SOLID"},
                }
            },
        )

    def delete_borders(self, range: str) -> None:
        """Removes borders of the cells by JSON format"""
        self.spreadsheet_to.worksheet(self.sheet_name_to).format(
            range,
            {
                "borders": {
                    "top": {"style": "None"},
                    "bottom": {"style": "None"},
                    "left": {"style": "None"},
                    "right": {"style": "None"},
                }
            },
        )

    def get_all_sheets_names(self, reverse=False):
        """This method returns worksheets names of doc"""
        months = {
            'январь': 1,
            'февраль': 2,
            'март': 3,
            'апрель': 4,
            'май': 5,
            'июнь': 6,
            'июль': 7,
            'август': 8,
            'сентябрь': 9,
            'октябрь': 10,
            'ноябрь': 11,
            'декабрь': 12,

        }
        result = []
        worksheet_names = self.spreadsheet_from.worksheets()
        for month in DataCollections.get_array_names(worksheet_names):
            if month.lower() in months:
                result.append(month)
        result.sort(key=lambda month_name: months[month_name.lower()])
        if reverse is True:
            result.reverse()
        return result

    def get_all_doc_values(self, worksheets_names: tuple or list, start_row: int = 2) -> list:
        """Gets worksheet names and save all values from them to list"""
        all_doc_values = []
        for item in worksheets_names:
            data = self.spreadsheet_from.worksheet(item).get_all_values()
            for single_list in data[start_row:]:
                if single_list[0] != "":
                    all_doc_values.append(single_list)
        return all_doc_values

    def delete_all_cells(self, sheet_id=None) -> None:
        """Removes all values form cells and cells borders by merge all cells and unmerge them"""
        unmerge_request = {
            "requests": [
                {
                    "unmergeCells": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 10,
                            "endRowIndex": 1000,
                            "startColumnIndex": 0,
                            "endColumnIndex": 6,
                        }
                    }
                }
            ]
        }
        merge_request = {
            "requests": [
                {
                    "mergeCells": {
                        "mergeType": "MERGE_ALL",
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 10,
                            "endRowIndex": 1000,
                            "startColumnIndex": 0,
                            "endColumnIndex": 6,
                        },
                    }
                }
            ]
        }

        self.spreadsheet_to.batch_update(merge_request)
        self.spreadsheet_to.batch_update(unmerge_request)

    def get_worksheet_by_name(self, worksheet_name: str):
        """Return worksheet object by name"""
        worksheet = self.spreadsheet_from.worksheet(worksheet_name)
        return worksheet

    def get_title_name(self):
        return self.spreadsheet_from.title
