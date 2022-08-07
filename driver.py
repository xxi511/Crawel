import os
import platform
import wget
import zipfile
import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def driver_name() -> str:
    sys = platform.system()
    return 'chromedriver.exe' if 'Windows' in sys else 'chromedriver'

def driver_zip_name() -> str:
    sys = platform.system()
    if 'Linux' in sys:
        return 'chromedriver_linux64.zip'
    elif 'Darwin' in sys:
        if 'x86_64' in platform.platform():
            return 'chromedriver_mac64.zip'
        else:
            return 'chromedriver_mac64_m1.zip'
    elif 'Windows' in sys:
        return 'chromedriver_win32.zip'

def download_driver(version: str):
    link = 'https://chromedriver.storage.googleapis.com/{}/{}'.format(version, driver_zip_name())
    file_name = wget.download(link)
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        file_path = os.getcwd() + '/' + driver_name()
        os.remove(file_path)
        zip_ref.extractall('./')
        subprocess.call(['chmod', 'u+x', file_path])
        os.remove(os.getcwd() + '/' + driver_zip_name())

def driver_path() -> str:
    return os.getcwd() + '/' + driver_name()

def get_selenium(href: str):
    options = Options()
    options.add_argument('headless')
    driver = webdriver.Chrome(driver_path(), chrome_options=options)
    driver.get(href)
    return driver
