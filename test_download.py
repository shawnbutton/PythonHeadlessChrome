from os import path, remove
from time import sleep

from driver_builder import DriverBuilder


class TestDownload:
    def test_download(self):

        driver_builder = DriverBuilder()

        download_path = path.dirname(path.realpath(__file__))

        expected_download = path.join(download_path, "5MB.zip")

        # clean downloaded file
        try:
            remove(expected_download)
        except OSError:
            pass

        assert (not path.isfile(expected_download))

        driver = driver_builder.get_driver(download_path, headless=True)

        driver.get("https://www.thinkbroadband.com/download")

        clone_box = driver.find_element_by_xpath('//*[@id="main-col"]/div/div/div[8]/p[1]/a/img')
        clone_box.click()

        # wait for download
        sleep(10)

        driver.close()

        assert (path.isfile(expected_download))

        print("done")
