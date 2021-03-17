import json
import time
import random

from fakemail import FakeMail

from seleniumwire import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

months = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

class DiscordTokenGenerator:
    def __init__(self, password):
        self.password = password

        self.fakemail = FakeMail()

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    def generate(self):
        try:
            self.fakemail.change()
            self.username = self.fakemail.address.split('@')[0]

            self.browser = webdriver.Chrome(chrome_options=self.chrome_options)

            self.browser.get('https://discord.com/register')

            self.__fill_register_form()
            self.__send_register_form()

            hcaptcha_bypassed = self.__bypass_hcatpcha()

            if not hcaptcha_bypassed:
                raise

            tag = self.__get_account_tag()
            token = self.__find_account_token()

            account_verified = self.__verify_account_email()

            if not account_verified:
                raise
            
            self.browser.quit()

            return {
                "success": True,

                "tag": tag,
                "token": token,
                "email": self.fakemail.address
            }

        except:
            self.browser.quit()
            return { "success": False }

    def __fill_register_form(self):
        email_field = WebDriverWait(self.browser, 15).until(EC.visibility_of_element_located((By.NAME, 'email')))
        email_field.send_keys(self.fakemail.address)

        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(self.username)

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(self.password)

        actions = ActionChains(self.browser)

        # fill form with a random day
        actions.send_keys(Keys.TAB)
        actions.send_keys(str(random.randint(0, 28)))

        # fill form with a random month
        actions.send_keys(Keys.TAB)
        actions.send_keys(str(random.choice(months)))

        # fill form with a random year
        actions.send_keys(Keys.TAB)
        actions.send_keys(random.randint(1980, 2003))

        actions.perform()

    def __send_register_form(self):
        try:
            continue_button = self.browser.find_element_by_class_name('button-3k0cO7')
            continue_button.click()

            limited_ip_error = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'errorMessage-1Zosc1')))
            
            if limited_ip_error == None:
                raise

            WebDriverWait(browser, 120).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'errorMessage-1Zosc1')))
            continue_button.click()

        except:
            pass

    def __bypass_hcatpcha(self):
        try:
            hcaptcha = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'alignCenter-1dQNNs')))
            
            iframe = hcaptcha.find_element_by_tag_name('iframe')
            print(iframe.get_attribute('innerHTML'))

            WebDriverWait(browser, 180).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'alignCenter-1dQNNs')))
        except:
            pass
        
        return True
        
    def __get_account_tag(self):
        id = WebDriverWait(self.browser, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'subtext-3CDbHg'))).text
        return f"{self.username}{id}"

    def __find_account_token(self):
        for request in self.browser.requests:
            token = request.headers['Authorization']
            if token != None and token != 'undefined':
                return token

        return

    def __verify_account_email(self):
        try:
            while len(self.fakemail.emails) <= 1:
                self.fakemail.refresh()

            bs4 = BeautifulSoup(self.fakemail.email(1), 'html.parser')
            verify_link = bs4.find('td', {'bgcolor': '#7289DA'}).a['href']

            self.browser.get(verify_link)

            back_button = WebDriverWait(self.browser, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'button-3k0cO7')))

            if back_button == None:
                raise

            return True

        except:
            return False