import os
import platform
from datetime import datetime

from selenium import webdriver

from selenium.webdriver.chrome.service import Service


class CreatBrowser:

    def __init__(self, dir_project):
        platform_to_os = platform.system()

        options = webdriver.ChromeOptions()

        if platform_to_os == "Linux":

            from xvfbwrapper import Xvfb

            vdisplay = Xvfb(width=1280, height=720)

            vdisplay.start()

            binary = self.get_chrome()

            options.binary_location = binary

            s = Service(executable_path=r"/usr/local/bin/chromedriver")


        else:

            s = Service(executable_path=f"{dir_project}\\src\\browser\\chromedriver.exe")

        options.add_argument("no-sandbox")

        options.add_argument(
            "--disable-application-cache")

        options.add_argument("window-size=1280,720")

        options.add_argument("--dns-prefetch-disable")

        options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome(service=s, options=options)

        try:
            browser_version = self.driver.capabilities['browserVersion']
            driver_version = self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
            print(
                f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Браузер: {browser_version} драйвер: {driver_version}')
        except:
            print(f'\nНе получилось определить версию uc браузера')

    def get_chrome(self):
        if os.path.isfile('/usr/bin/chromium-browser'):
            return '/usr/bin/chromium-browser'
        elif os.path.isfile('/usr/bin/chromium'):
            return '/usr/bin/chromium'
        elif os.path.isfile('/usr/bin/chrome'):
            return '/usr/bin/chrome'
        elif os.path.isfile('/usr/bin/google-chrome'):
            return '/usr/bin/google-chrome'
        else:
            return None
