import time
from selenium.webdriver.common.by import By

from src.school.load_page import LoadPage


class JobCabinet:
    def __init__(self, driver):
        self.driver = driver
        self.source_name = 'Uchebnik'

    def get_name_cabinet(self):
        count = 0

        count_try = 3

        while True:

            count += 1

            if count > count_try:
                print(f'Не смог прочесть статус кабинета')
                return False

            try:
                _name = self.driver.find_element(by=By.XPATH,
                                                 value=f"//div[contains(@class, 'userMenu')]").text
            except:

                time.sleep(1)

                continue

            return _name

    def click_in_cabinet(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@class, 'userMenu')]//button").click()

        except:
            return False

        return True

    def check_open_popup_cabinet(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//main//*[contains(@class, 'userName')]")
        except:
            return False

        return True

    def open_change_menu(self):
        count = 0
        count_try = 10
        while True:
            count += 1
            if count > count_try:
                print(f'Не смог переключить открыть меню для смены кабинета')
                return False

            res_click = self.click_in_cabinet()

            status_popup = self.check_open_popup_cabinet()

            if not status_popup:
                if count > 1:
                    time.sleep(1)
                continue

            return True

    def get_el_cabinet_name(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//main//li[@data-type='teacher']").click()

        except:
            return False

        return True

    def insert_cabinet(self):

        el_cabinet = self.get_el_cabinet_name()

        if not el_cabinet:
            return False

        return True

    def change_cabinet(self):
        open_popup = self.open_change_menu()

        if not open_popup:
            return False

        res_insert_cabinet_name = self.insert_cabinet()

        return res_insert_cabinet_name

    def loop_change_cabinet(self, name_cabinet):

        change = False

        count = 0
        count_try = 3
        while True:
            count += 1
            if count > count_try:
                print(f'Не смог переключить кабинет на {name_cabinet}')
                return False

            _name_cabinet = self.get_name_cabinet()

            if name_cabinet.lower() not in _name_cabinet.lower():
                res_change = self.change_cabinet()

                if res_change:
                    change = True

                if count > 1:
                    time.sleep(1)

                continue

            if change:
                url = 'https://uchebnik.mos.ru/catalogue'

                res_load = LoadPage(self.driver, url).loop_load_page("//*[contains(text(), 'Тесты')]")

                if not res_load:
                    continue

            return True

    def start_job_cabinet(self, name_cabinet):
        res_change = self.loop_change_cabinet(name_cabinet)

        return res_change

    def check_name_cabinet(self, name_cabinet):
        _name_cabinet = self.get_name_cabinet()

        if name_cabinet.lower() not in _name_cabinet.lower():
            return False

        return True
