import os
import sys

from selenium.webdriver import Chrome
from selenium.webdriver.chrome import webdriver as chrome_webdriver


class DriverBuilder():
    def get_driver(self, download_location=None, headless=False):

        driver = self._get_chrome_driver(download_location, headless)

        driver.set_window_size(1400, 700)

        return driver

    def _get_chrome_driver(self, download_location, headless):
        chrome_options = chrome_webdriver.Options()
        if download_location:
            prefs = {'download.default_directory': download_location,
                     'download.prompt_for_download': False,
                     'download.directory_upgrade': True,
                     'safebrowsing.enabled': False,
                     'safebrowsing.disable_download_protection': True}

            chrome_options.add_experimental_option('prefs', prefs)

        if headless:
            chrome_options.add_argument("--headless")

        dir_path = os.path.dirname(os.path.realpath(__file__))
        driver_path = os.path.join(dir_path, "drivers/chromedriver")

        if sys.platform.startswith("win"):
            driver_path += ".exe"

        driver = Chrome(executable_path=driver_path, chrome_options=chrome_options)

        if headless:
            self.enable_download_in_headless_chrome(driver, download_location)

        return driver

    def enable_download_in_headless_chrome(self, driver, download_dir):
        """
        there is currently a "feature" in chrome where
        headless does not allow file download: https://bugs.chromium.org/p/chromium/issues/detail?id=696481
        This method is a hacky work-around until the official chromedriver support for this.
        Requires chrome version 62.0.3196.0 or above.
        """

        # add missing support for chrome "send_command"  to selenium webdriver
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        command_result = driver.execute("send_command", params)
        print("response from browser:")
        for key in command_result:
            print("result:" + key + ":" + str(command_result[key]))
