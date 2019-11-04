# Project : LansWeeper
# Created by Moncef BENAICHA at 7/24/18 - 22:01
# Email : contact@moncefbenaicha.me

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import sys
import shutil

dir_path = os.path.dirname(os.path.realpath(__file__))
#dir_path = os.path.dirname(os.path.realpath(sys.executable))


class Browser(object):

    def __init__(self):
        options = Options()
        options.add_argument('user-data-dir='+dir_path+"/navigator/")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-default-apps")
        options.add_argument("test-type=browser")
        options.add_argument("disable-infobars")
        prefs = {'download.default_directory': dir_path}
        options.add_experimental_option('prefs', prefs)
        self.browser = webdriver.Chrome(chrome_options=options, executable_path=dir_path+"/chromedriver.exe")
        print('Browser started')

    def open_page(self, link):
        self.browser.get(link)

    def getContent(self, link):
        self.open_page(link)
        time.sleep(5)
        return self.browser.page_source

    def getSource(self):
        return self.browser.page_source

    def sendClick(self, way):
        self.browser.find_element_by_xpath(way).click()

    def sendData(self, data, destination, submit=False):
        to = self.browser.find_element_by_xpath(destination)
        to.send_keys(data)
        if submit:
            to.send_keys(Keys.ENTER)
            time.sleep(5)

    def sendActionChain(self, elements):
        ActionChains(self.browser).key_down(Keys.COMMAND).click(self.browser.find_element_by_xpath(elements[0])).click(self.browser.find_element_by_xpath(elements[1])).key_up(Keys.COMMAND).perform()

    def alertHandling(self):
        try:
            alert = self.browser.switch_to.alert
            alert.accept()
        except:
            print("No alert found passing")

    def exit(self):
        self.browser.close()
        time.sleep(2)
        shutil.rmtree(dir_path+"/navigator/")

    def __del__(self):
        self.exit()
