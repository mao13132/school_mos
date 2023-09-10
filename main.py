import os
from datetime import datetime

from src.browser.createbrowser import CreatBrowser
from src.school.iter_requests import IterRequests
from src.school.start_school import StartSchool


def main():
    dir_project = os.getcwd()

    try:

        browser = CreatBrowser(dir_project)

        res_job = StartSchool(browser.driver).start_school()

        res_iter_requests = IterRequests(browser.driver, dir_project).start_iter()

    finally:
        browser.driver.quit()


if __name__ == '__main__':
    print(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} начал работу')

    main()

    print(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} закончил работу')
