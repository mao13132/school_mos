import os
import time
from datetime import datetime
from json import dump

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import REQUESTS_LIST
from src.school.job_post import JobPost
from src.school.load_page import LoadPage
from src.school.start_uchebnik import StartUchebnik


class IterRequests:
    def __init__(self, driver, dir_project):
        self.driver = driver
        self.dir_project = dir_project

    def write_request(self, request):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@class, 'searchField')]/input").send_keys(request)

            time.sleep(5)

            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@class, 'searchField')]/input").send_keys(Keys.ENTER)

        except:
            print(f'Не удалось вписать запрос "{request}"')

            return False

        return True

    def check_load_data_by_request(self):

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

    def load_one_post(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@class, 'styles_materials')]"
                                           f"//*[contains(@class, 'styles_material')]"
                                           f"//a").click()

        except:
            print(f'Нет материалов согласно запросу')
            return False

        return True

    def check_load_page(self, _xpatch):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, _xpatch)))
            return True
        except:

            res_load = LoadPage(self.driver, 'https://school.mos.ru') \
                .loop_load_page("//*[contains(text(), 'Тесты')]")

            return False

    def loop_check_load(self):

        count = 0

        count_try = 60

        while True:

            count += 1

            if count > count_try:
                print(f'Не исчезает загрузка')
                return False

            try:
                self.driver.find_element(by=By.XPATH,
                                         value=f"//*[contains(@class, 'contextContainer')]//button")

                return True
            except:
                time.sleep(1)
                continue

    def save_to_json(self, good_dict):
        try:
            file_name = os.path.join(self.dir_project, 'good', f'{datetime.now().strftime("%Y.%m.%d %H.%M.%S")}.json')

            with open(file_name, 'w', encoding='utf-8') as file:
                dump(good_dict, file, indent=4, ensure_ascii=False)
        except:
            return False

        return file_name

    def iter_requests(self):
        for _req in REQUESTS_LIST:

            res_job = StartUchebnik(self.driver).start_uchebnik()

            res_write = self.write_request(_req)

            time.sleep(1)

            if not self.check_load_data_by_request():
                continue

            res_click = self.load_one_post()

            self.check_load_page("//*[contains(@class, 'materialContainer')]")

            res_load = self.loop_check_load()

            if not res_load:
                return False

            good_dict = JobPost(self.driver).start_job_post(_req)

            res_save = self.save_to_json(good_dict)

            print(f'Сохранил результат обработки запроса "{_req}" в файл {res_save}')

        return True

    def start_iter(self):

        res_iter = self.iter_requests()

        return True
