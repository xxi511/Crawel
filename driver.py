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
        if is_driver_exist():
            os.remove(driver_path())
        zip_ref.extractall('./')
        if platform.system() != 'Windows':
            subprocess.call(['chmod', 'u+x', driver_path()])
    zip_path = os.path.join(os.getcwd(), driver_zip_name())
    if os.path.exists(zip_path):
        os.remove(zip_path)

def driver_path() -> str:
    return os.path.join(os.getcwd(), driver_name())

def is_driver_exist() -> bool:
    path = driver_path()
    return os.path.exists(path)

def get_chrome_version() -> str:
    sys = platform.system()
    if 'Linux' in sys:
        path = ''
        return 'unknown'
    elif 'Darwin' in sys:
        path = ''
        return 'unknown'
    elif 'Windows' in sys:
        path = 'C:\Program Files (x86)\Google\Chrome\Application'
        return os.listdir(path)[0]

def get_selenium(href: str):
    options = Options()
    options.add_argument('headless')
    driver = webdriver.Chrome(driver_path(), chrome_options=options)
    driver.get(href)
    return driver
