import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import LOGIN, PASSWORD
from src.school.load_page import LoadPage


class StartSchool:
    def __init__(self, driver):
        self.driver = driver

    def check_good_auth(self, _xpatch):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, _xpatch)))
            return True
        except:
            return False

    def click_in(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@class, 'login_action')]").click()
        except:
            print(f'Не смог кликнуть на кнопку "Войти"')
            return False

        return True

    def click_form_login(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//button[contains(@class, 'form-login')]").click()
        except:
            print(f'Не смог кликнуть на кнопку "Войти" на форме')
            return False

        return True

    def check_load_in(self):

        count = 0

        count_try = 60

        while True:

            count += 1

            if count > count_try:
                return False

            try:
                value = self.driver.find_element(by=By.XPATH,
                                                 value=f"//*[contains(@class, 'system-main__form')]").get_attribute(
                    'style')
            except:
                continue

            if 'none' in value:
                continue

            return True

    def write_value(self, value, patch):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=patch).send_keys(value)
        except:
            print(f'Не удалось вписать "{value}"')

            return False

        return True

    def start_school(self):
        url = 'https://school.mos.ru'

        res_load = LoadPage(self.driver, url).loop_load_page("//*[contains(@class, 'login_title')]")

        if not res_load:
            return False

        print(f'Успешно зашёл на целевой сайт')

        res_click = self.click_in()

        if not res_click:
            return False

        if not self.check_load_in():
            return False

        res_write_login = self.write_value(LOGIN, f"//input[@name='login']")

        res_write_login = self.write_value(PASSWORD, f"//input[@name='password']")

        time.sleep(1)

        res_click = self.click_form_login()

        if not res_click:
            return False

        res_auth = self.check_good_auth(f"//*[contains(@class, 'client-profile')]")

        return True
