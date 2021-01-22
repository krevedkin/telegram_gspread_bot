# script version 1.1
import datetime


class DataCollections:
    """Class for work with lists, lists of lists and other collections of data"""

    @staticmethod
    def list_sort(list_for_sorting: list, sorting_queue: tuple[int] or list[int]) -> list:
        """Gets single list,and list of indexes and return new list with elements saved and ordered by sorting_queue"""
        result_list = []
        for index in sorting_queue:
            result_list.append(list_for_sorting[index])
        return result_list

    def create_head_dates(self, first_date: str = "10.05.20", second_date: str = "15.05.20") -> tuple:
        """Creates two strings like '10 may 2020' from '10.05.2020"""
        months = {
            "01": "Января",
            "02": "Февраля",
            "03": "Марта",
            "04": "Апреля",
            "05": "Мая",
            "06": "Июня",
            "07": "Июля",
            "08": "Августа",
            "09": "Сетнября",
            "10": "Октября",
            "11": "Ноября",
            "12": "Декабря",
        }

        first_date = first_date.split(".")
        second_date = second_date.split(".")

        day_first = first_date[0]
        month_first = first_date[1]
        if len(first_date[2]) == 4:
            year_first = first_date[2]
        else:
            year_first = "20" + first_date[2]
        day_second = second_date[0]
        month_second = second_date[1]
        if len(second_date[2]) == 4:
            year_second = second_date[2]
        else:
            year_second = "20" + second_date[2]

        result_first_string = f"{day_first} {months[month_first]} {year_first}"
        result_second_string = f"{day_second} {months[month_second]} {year_second}"
        return result_first_string, result_second_string

    def return_row_index(self, insert_list: list[list]) -> list:
        """Returns a list of indices for strings that start with a specific word"""
        row_index_list = []
        for row_index, single_list in enumerate(insert_list):
            if single_list[0] == "Дата":
                row_index_list.append(row_index + 1)
            else:
                row_index += 1
        return row_index_list

    def create_sorted_list_of_lists(self, list_of_lists: list[list],
                                    sorting_queue: tuple[int] or list[int],
                                    flag=True) -> list[list]:
        """Gets list of lists with all values, and list of indices which should be saved by order of sorting_queue"""
        result_list = []
        first_index_of_list = ""
        stupid_free_spaces = ""  # это КОСТЫЛЬ, чтобы вставить 2 пустых строки в список
        # и они корректно вставлялись в объединенные ячейки
        for single_list in list_of_lists:
            first_day_and_month = self.date(single_list[0])
            if first_index_of_list != first_day_and_month and flag is True:
                first_index_of_list = first_day_and_month
                result_list.append(
                    ["Дата", stupid_free_spaces, stupid_free_spaces, single_list[0]]
                )
                result_list.append(self.list_sort(single_list, sorting_queue))
            else:
                result_list.append(self.list_sort(single_list, sorting_queue))
        return result_list

    def date(self, item: str) -> object or None:
        """Creates a datetime class object from string"""
        try:
            check_len = item.split(".")
            if len(check_len[2]) == 4:
                item = datetime.datetime.strptime(item, "%d.%m.%Y")
            else:
                item = datetime.datetime.strptime(item, "%d.%m.%y")
            return item
        except:
            return None

    def first_date_search(self, list_for_search: list[list], item: str) -> int or None:
        """Searching for the first value in the list. It uses binary search algorithm"""
        min = 0
        max = len(list_for_search) - 1
        searched_item = self.date(item)

        while max >= min:
            mid = (min + max) // 2
            guess = self.date(list_for_search[mid][0])
            try:
                previous_value = self.date(list_for_search[mid - 1][0])
            except:
                return mid
            if guess == searched_item and guess != previous_value:
                return mid
            elif guess == searched_item and guess == previous_value:
                max = mid - 1
            elif guess > searched_item:
                max = mid - 1
            else:
                min = mid + 1
        return None

    def last_date_search(self, list_for_search: list[list], item: str) -> int or None:
        """Searching for the last value in the list. It uses binary search algorithm"""
        min = 0
        max = len(list_for_search) - 1
        searched_item = self.date(item)

        while max >= min:
            mid = (min + max) // 2
            guess = self.date(list_for_search[mid][0])
            try:
                next_value = self.date(list_for_search[mid + 1][0])
            except:
                return mid
            if guess == searched_item and guess != next_value:
                return mid
            elif guess == searched_item and guess == next_value:
                min = mid + 1
            elif guess > searched_item:
                max = mid - 1
            else:
                min = mid + 1
        return None

    @staticmethod
    def get_array_names(worksheets_names, array):
        """Gets list of strings from gspread_worksheets method
         and saves their names in the list if name exists in array"""
        result_worksheet_names = []
        array_checker = array
        for item in worksheets_names:
            item = str(item)
            item = item.split("'")
            if item[1] in array_checker:
                result_worksheet_names.append(item[1])
        return result_worksheet_names

    def string_finder(self, string: str, start_find: str, second_find: str, step: int = 0) -> str:
        """Searching for specific value in the string"""
        first_index = string.find(start_find)
        second_index = string.find(second_find)
        result = string[first_index + 1:second_index - step]
        return result

    def quick_sort(self, list_of_lists: list[list]) -> list[list]:
        """QuickSort algorithm for sorting list of lists in ascending order"""
        if len(list_of_lists) <= 1:
            return list_of_lists

        else:
            left = []
            center = []
            right = []
            elem = list_of_lists[0][0]
            try:
                elem = int(self.string_finder(elem, "(", ")", step=4))
            except ValueError:
                try:
                    elem = int(self.string_finder(elem, "(", ")", step=6))
                except ValueError:
                    print("Проблема тут")

            for single_list in list_of_lists:
                try:
                    value = int(self.string_finder(single_list[0], "(", ")", step=4))
                except ValueError:
                    try:
                        value = int(self.string_finder(single_list[0], "(", ")", step=6))
                    except ValueError:
                        print("Не является целочисленным числом")
                if value < elem:
                    left.append(single_list)
                elif value > elem:
                    right.append(single_list)
                else:
                    center.append(single_list)
            return self.quick_sort(left) + center + self.quick_sort(right)

    def insert_data_to_list(self, list_of_lists: list[list], index: int) -> None:
        """Method for insert value to the single list in list of lists"""
        for single_list in list_of_lists:
            data = self.string_finder(single_list[0], "(", ")")
            single_list.insert(index, data)
