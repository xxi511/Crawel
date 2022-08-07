from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

import zipfile
import wget
import platform
import os
import subprocess

class Forum:
    def __init__(self) -> None:
        self.driver = None
        pass

    def driver_name(self) -> str:
        sys = platform.system()
        return 'chromedriver.exe' if 'Windows' in sys else 'chromedriver'

    def driver_zip_name(self) -> str:
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

    def getTid(self, url: str) -> str:
        pattern = re.compile(r'tid=[0-9]+')
        tid = pattern.search(url).group()
        return tid[4:]

    def prepare_driver(self):
        options = Options()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome('./' + self.driver_name(), chrome_options=options)
        chrome_version = driver.capabilities['browserVersion']
        driver_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
        if chrome_version.split('.')[0] != driver_version.split('.')[0]: 
            print('提示！ driver 版本錯誤，下載新版本中，請稍候')
            driver.quit()
            self.download_driver(chrome_version)
        
        driver.set_window_size(1024, 960)
        driver.get("https://woodo.club/forum.php")
        self.driver = driver

    def download_driver(self, version: str):
        link = 'https://chromedriver.storage.googleapis.com/{}/{}'.format(version, self.driver_zip_name())
        file_name = wget.download(link)
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            file_path = os.getcwd() + '/' + self.driver_name()
            os.remove(file_path)
            zip_ref.extractall('./')
            subprocess.call(['chmod', 'u+x', file_path])
            os.remove(os.getcwd() + '/' + self.driver_zip_name())
            self.prepare_driver()
    
    def login(self, account: str, password: str):
        driver = self.driver
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "lsform"))
        )
        driver.find_element_by_css_selector('#ls_username').send_keys(account)
        time.sleep(1)
        driver.find_element_by_css_selector('#ls_password').send_keys(password)
        time.sleep(1)
        driver.find_element_by_css_selector('#lsform td.fastlg_l button').click()
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.avt.y"))
            )
        except:
            driver.quit()
            raise ValueError('Login failed')
    
    def postCover(self, postLink, banner, title, author, state, desc, subCategoryIdx):
        driver = self.driver
        _title = '{} 作者：{} {}'.format(title, author, state)
        content = """[img]{}[/img]
【作者概要】：

【小說類型】：

【內容簡介】：
　　{}

【其他作品】：""".format(banner, desc)

        driver.get(postLink)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "subject"))
            )
            driver.find_element_by_css_selector('#extra_tag_chk').click()
            driver.find_element_by_css_selector('#tags').send_keys(author)
            driver.find_element_by_css_selector('#subject').send_keys(_title)
            driver.find_element_by_css_selector('#e_textarea').send_keys(content)
            self.setSubCategory(driver, subCategoryIdx)
            driver.find_element_by_css_selector('#postsubmit').click()
            return self.checkPostState()
        except:
            return 'failed, post novel conver'

    def setSubCategory(self, subCategoryIdx):
        driver = self.driver
        try:
            ulEle = driver.find_element_by_css_selector('#typeid_ctrl_menu')
            style = 'width: 80px; position: absolute; z-index: 301; left: 7.2px; top: 298.6px;'
            driver.execute_script(
                "arguments[0].setAttribute('style', arguments[1])", ulEle, style)
            eles = driver.find_elements_by_css_selector('#typeid_ctrl_menu ul li')
            for idx, li in enumerate(eles):
                if idx == subCategoryIdx:
                    li.click()
        except:
            print('a')

    def checkPostState(self):
        driver = self.driver
        time.sleep(1)
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "postlist"))
            )
            url = driver.current_url
            return self.getTid(url)
        except:
            return 'failed, check post state'


    def postArticle(self, postLink, content):
        driver = self.driver
        driver.get(postLink)
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "e_textarea"))
            )
            areaEle = driver.find_element_by_css_selector('#e_textarea')
            driver.execute_script(
                "arguments[0].value = arguments[1]", areaEle, content)
            time.sleep(1)
            driver.find_element_by_css_selector('#postsubmit').click()
            return self.checkPostState()
        except:
            return 'failed, post novel article'