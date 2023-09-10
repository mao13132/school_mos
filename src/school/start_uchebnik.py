import time

from selenium.webdriver.common.by import By

from src.school.job_cabinet import JobCabinet
from src.school.load_page import LoadPage


class StartUchebnik:
    def __init__(self, driver):
        self.driver = driver

    def click_test(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(text(), 'Тесты')]").click()

        except:
            print(f'Не смог кликнуть на кнопку "Войти"')
            return False

        return True

    def check_set_tests(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@class, 'checkboxIconCheckChecked')]//parent::label")

        except:
            return False

        return True

    def check_load_filter(self):

        count = 0

        count_try = 60

        while True:

            count += 1

            if count > count_try:
                return False

            try:
                self.driver.find_element(by=By.XPATH,
                                         value=f"//*[contains(@class, 'materialType')]//*[contains(text(), 'Тесты')]")
            except:
                continue

            return True

    def check_load_icon(self):

        count = 0

        count_try = 60

        while True:

            count += 1

            if count > count_try:
                print(f'Не исчезает загрузка')
                return False

            try:
                self.driver.find_element(by=By.XPATH,
                                         value=f"//*[contains(@class, 'styles_loader')]")

                time.sleep(1)

                continue
            except:
                return True

    def start_uchebnik(self):
        url = 'https://uchebnik.mos.ru/catalogue'

        res_load = LoadPage(self.driver, url).loop_load_page("//*[contains(text(), 'Тесты')]")

        if not res_load:
            return False

        print(f'Успешно зашёл на сайт uchebnik')

        check_active_test = self.check_set_tests()

        if not check_active_test:
            res_click = self.click_test()

        if not self.check_load_filter():
            return False

        self.check_load_icon()

        JobCabinet(self.driver).start_job_cabinet('Учитель')

        return True
