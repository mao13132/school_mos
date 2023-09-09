import os
from datetime import datetime

from src.browser.createbrowser import CreatBrowser
from src.school.iter_requests import IterRequests
from src.school.start_school import StartSchool
from src.school.start_uchebnik import StartUchebnik


def main():
    dir_project = os.getcwd()

    try:

        browser = CreatBrowser(dir_project)

        res_job = StartSchool(browser.driver).start_school()

        res_job = StartUchebnik(browser.driver).start_uchebnik()

        res_iter_requests = IterRequests(browser.driver, dir_project).start_iter()

    finally:
        browser.driver.quit()

    print()


print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} BoosterSeo: начал работу')

if __name__ == '__main__':
    main()
