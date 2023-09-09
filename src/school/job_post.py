import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from src.school.load_page import LoadPage


class JobPost:
    def __init__(self, driver):
        self.driver = driver
        self.good_job = {}

    def loop_two_window(self):

        count = 0

        count_try = 60

        while True:

            count += 1

            if count > count_try:
                print(f'Не открылось окно')
                return False

            try:
                count_windows = len(self.driver.window_handles)

                if count_windows > 1:
                    return True

                time.sleep(1)

                continue
            except:
                continue

    def get_rows(self):
        _rows = self.driver.find_elements(by=By.XPATH,
                                          value=f"//*[contains(@class, 'Overlay-wrapper')]//*[contains(@id, 'task')]")

        return _rows

    def loop_get_rows(self):

        count = 0

        count_try = 3

        while True:

            count += 1

            if count > count_try:
                print(f'Не смог получить строчки')
                return False

            try:
                _rows = self.get_rows()

                if _rows != []:
                    return _rows

                time.sleep(1)

                continue
            except:
                continue

    def click_look(self):
        try:
            self.driver.find_elements(by=By.XPATH,
                                      value=f"//*[contains(@class, 'contextContainer')]//button")[0].click()
        except:
            return False

        return True

    def click_show_rows(self):

        count = 0

        count_try = 60

        while True:

            count += 1

            if count > count_try:
                print(f'Не смог получить строчки')
                return False

            try:
                self.driver.find_elements(by=By.XPATH,
                                          value=f"//*[contains(@class, 'infoWrapper')]//button")[0].click()

                return True
            except:
                time.sleep(1)
                continue

    def show_row(self, row):
        try:
            row.find_element(by=By.XPATH,
                             value=f".//button").click()
        except:
            return False

        return True

    def get_keys_text_by_row(self, row):
        try:
            keys_ = row.find_element(by=By.XPATH,
                                     value=f".//*[contains(@class, 'TaskAnswerView-text')]").text
        except:
            return ''

        return keys_

    def get_value_by_radiobox(self, row):
        try:
            elements = row.find_element(by=By.XPATH,
                                        value=f".//span[contains(@class, 'Mui-checked')]//following-sibling::label").text
        except:
            return ''

        return elements

    def get_value_by_show_rows(self, row):
        try:
            elements = row.find_element(by=By.XPATH,
                                        value=f".//*[contains(@class, 'MuiOutlinedInput')]"
                                              f"//*[contains(@class, 'MuiTypography')]").text

        except:
            return ''

        return elements

    def get_value_by_obe_to_one(self, row):
        try:
            elements = row.find_element(by=By.XPATH,
                                        value=f".//*[contains(@class, 'MuiCollapse-wrapper')]"
                                              f"//*[contains(@class, 'MuiCollapse-vertical')]")


        except:
            return ''

        return elements.screenshot_as_base64

    def get_type_row(self, row):
        try:
            elements = row.find_element(by=By.XPATH,
                                        value=f".//p[contains(@class, 'MuiTypography')]").text
        except:
            return ""

        return elements

    def get_response_row(self, row):
        # TODO функция определения типа ответа
        type_row = self.get_type_row(row)

        if type_row == 'Одиночный выбор':
            value = self.get_value_by_radiobox(row)
        elif type_row == 'Выпадающий список':
            value = self.get_value_by_show_rows(row)
        elif type_row == 'Один к одному':
            value = self.get_value_by_obe_to_one(row)
        else:
            print(f'Не смог определить тип строки')
            value = ''

        return value

    def iter_rows(self, list_rows):
        for count, row in enumerate(list_rows):
            res_show = self.show_row(row)

            if not res_show:
                print(f'Строка {count + 1} не раскрылась')
                continue

            _keys = self.get_keys_text_by_row(row)

            _value = self.get_response_row(row)

            if _value == '':
                continue

            self.good_job[_keys] = _value

            print()

        return True

    def start_job_post(self, _req):

        print(f'Зашёл в материал по запросу "{_req}"')

        res_click = self.click_look()

        res_loop = self.loop_two_window()

        if not res_click:
            return False

        self.driver.switch_to.window(self.driver.window_handles[1])

        res_click = self.click_show_rows()

        list_rows = self.loop_get_rows()

        if not list_rows:
            return False

        res_iter = self.iter_rows(list_rows)

        print()

        return self.good_job
