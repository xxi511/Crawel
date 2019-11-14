from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import platform


def getTid(url):
    pattern = re.compile(r'tid=[0-9]+')
    tid = pattern.search(url).group()
    return tid[4:]


def getDriverPath():
    sys = platform.system()
    if 'Linux' in sys:
        return './driver/linux_chromedriver'
    elif 'Darwin' in sys:
        return './driver/mac_chromedriver'
    elif 'Windows' in sys:
        return './driver/win_chromedriver.exe'


def openForum(forumDomain, account, password):
    options = Options()
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(getDriverPath(), chrome_options=options)
    driver.set_window_size(1024, 960)
    driver.get("http://woodo.epizy.com/forum.php")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "lsform"))
        )
        login(driver, account, password)
        return driver
    except:
        driver.quit()
        raise ValueError('Open forum failed')


def login(driver, account, password):
    driver.find_element_by_css_selector('#ls_username').send_keys(account)
    driver.find_element_by_css_selector('#ls_password').send_keys(password)
    driver.find_element_by_css_selector('#lsform td.fastlg_l button').click()
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.avt.y"))
        )
        return driver
    except:
        driver.quit()
        raise ValueError('Login failed')


def postCover(driver, postLink, banner, title, author, state, desc, subCategoryIdx):
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
        setSubCategory(driver, subCategoryIdx)
        driver.find_element_by_css_selector('#postsubmit').click()
        return checkPostState(driver)
    except:
        return 'failed, post novel conver'
        # driver.quit()
        # raise ValueError('post novel cover failed')

def setSubCategory(driver, subCategoryIdx):
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

def checkPostState(driver):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "postlist"))
        )
        url = driver.current_url
        return getTid(url)
    except:
        return 'failed, check post state'
        # driver.quit()
        # raise ValueError('post novel failed')


def postArticle(driver, postLink, content):
    driver.get(postLink)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "e_textarea"))
        )
        areaEle = driver.find_element_by_css_selector('#e_textarea')
        driver.execute_script(
            "arguments[0].value = arguments[1]", areaEle, content)
        driver.find_element_by_css_selector('#postsubmit').click()
        return checkPostState(driver)
    except:
        return 'failed, post novel article'
        # driver.quit()
        # raise ValueError('post novel article failed')
