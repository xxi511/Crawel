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
        return 'linux64/chromedriver-linux64.zip'
    elif 'Darwin' in sys:
        if 'x86_64' in platform.platform():
            return 'mac-arm64/chromedriver-mac-arm64.zip'
        else:
            return 'mac-x64/chromedriver-mac-x64.zip'
    elif 'Windows' in sys:
        return 'win64/chromedriver-win64.zip'

def download_driver(version: str):
    link = 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{}/{}'.format(version, driver_zip_name())
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
    path = os.path.join(os.getcwd(), driver_name())
    if os.path.exists(path):
        return  path
    else:
        parent = os.pardir
        path = os.path.join(parent, driver_name())
        return  path

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
    options.add_argument('--headless')
    driver = webdriver.Chrome(driver_path(), chrome_options=options)
    driver.get(href)
    return driver

if __name__ == '__main__':
    a = driver_path()