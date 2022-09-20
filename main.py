import json
import os
import time

from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class WeatherShopper:
    def __init__(self, data):
        """Initialize data"""
        s = Service('/Users/swaggy/Downloads/chromedriver')
        load_dotenv()
        self.driver = webdriver.Chrome(service=s)
        self.email = data['email']
        self.card_number = os.getenv('CARD_NUMBER')
        self.card_year = os.getenv('CARD_YEAR')
        self.cvc = os.getenv('CVC')
        self.zipcode = os.getenv('ZIPCODE')

    def start_website(self):
        """Open browser and search for WeatherShopper"""
        self.driver.get('https://weathershopper.pythonanywhere.com/')
        self.driver.maximize_window()

    def get_current_temp(self):
        """Determine if user needs sunscreen or moisturizer based on the temperature"""
        temperature = self.driver.find_element(By.ID, 'temperature').text
        current_temp = ""

        for num in temperature:
            if num.isdigit():
                current_temp += num

        if int(current_temp) <= 19:
            #Click Moisturizer Button
            self.driver.find_element(By.XPATH,'/html/body/div/div[3]/div[1]/a/button').click()
            print('The current temperature is currently ' + temperature)
            print("Don't let cold weather ruin your skin. Use your favourite moisturizer and keep your skin stay young.")
        else:
            #Click Sunscreen Button
            self.driver.find_element(By.XPATH,'/html/body/div/div[3]/div[2]/a/button').click()
            print('The current temperature is currently ' + temperature)


    def moisturizer(self):
        """Add two moisturizers to your cart. First, select the least expensive mositurizer that contains Aloe.
        For your second moisturizer, select the least expensive moisturizer that contains almond.
        Click on cart when you are done."""


    def sunscreen(self):
        """Add two sunscreens to your cart. First, select the least expensive sunscreen that is SPF-50.
        For your second sunscreen, select the least expensive sunscreen that is SPF-30.
        Click on the cart when you are done."""

        self.driver.get('https://weathershopper.pythonanywhere.com/sunscreen')
        sunscreens = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/h2').text
        if sunscreens == 'Sunscreens':
            print("Treat your skin right. Don't leave your home without your favorite sunscreen. Say goodbye to sunburns.")
        else:
            return None

    def get_spf_30(self):
        """Get spf_30"""
        self.current_spf_30 = []
        sunscreen = self.driver.find_elements(By.XPATH, "//*[contains(text(),'SPF-30') or \
        contains(text(),'spf-30')]/following-sibling::p")

        for spf in sunscreen:
            for cheapest_spf30 in spf.text.split():
                if cheapest_spf30.isdigit():
                    self.current_spf_30.append(cheapest_spf30)
                    self.current_spf_30.sort()

        self.driver.find_element(By.XPATH, "//*[contains(text(),'SPF-30') or \
        contains(text(),'spf-30')]/following-sibling::p[contains(text(),%s)]/following-sibling::\
            button[text() = 'Add']" % self.current_spf_30[0]).click()

        print("Currently the cheapest SPF-30 sunscreen is priced at: " + self.current_spf_30[0])

    def get_spf_50(self):
        """Get spf_50"""
        self.current_spf_50 = []
        sunscreen = self.driver.find_elements(By.XPATH, "//*[contains(text(),'SPF-50') or \
        contains(text(),'spf-50')]/following-sibling::p")

        for spf in sunscreen:
            for cheapest_spf50 in spf.text.split():
                if cheapest_spf50.isdigit():
                    self.current_spf_50.append(cheapest_spf50)
                    self.current_spf_50.sort()

        self.driver.find_element(By.XPATH, "//*[contains(text(),'SPF-50') or \
        contains(text(),'spf-50')]/following-sibling::p[contains(text(),%s)]/following-sibling::\
            button[text() = 'Add']" % self.current_spf_50[0]).click()
        print("Currently the cheapest SPF-50 sunscreen is priced at: " + self.current_spf_50[0])


    def cart_click_and_purchase(self):
        """Verify items are correct and go to payment form"""
        self.driver.find_element(By.CLASS_NAME, 'thin-text.nav-link').click()
        cheapest_sunscreens = []
        sunscreens = self.driver.find_elements(By.XPATH, "//*[contains(text(),'SPF') or \
                contains(text(),'spf')]/following-sibling::td")

        for sunscreen in sunscreens:
           current_sunscreen = sunscreen.text
           cheapest_sunscreens.append(current_sunscreen)

        if self.current_spf_30[0] and self.current_spf_50[0] in cheapest_sunscreens:
            print("Processing your order for both sunscreen lotions now.")
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/button/span').click()

    def card_payment(self):
        """Input card information from Stripe"""

        """
        wait = WebDriverWait(self.driver, 30)
        email = wait.until(EC.element_to_be_clickable((By.ID, 'email')))
        email.send_keys('Test Keys')

        card_number = self.driver.find_element(By.ID, 'card_number')
        card_number.send_keys(self.card_number)

        card_year = self.driver.find_element(By.ID, 'cc-exp')
        card_year.send_keys(self.card_year)

        card_cvc = self.driver.find_element(By.ID, 'cc-csc')
        card_cvc.send_keys(self.cvc)

        zipcode = self.driver.find_element(By.ID, 'billing-zip')
        zipcode.send_keys(self.zipcode)
        """

    def run_automation(self):
        self.start_website()
        self.get_current_temp()
        time.sleep(3)
        self.sunscreen()
        self.get_spf_30()
        self.get_spf_50()
        self.cart_click_and_purchase()
        time.sleep(2)
        self.card_payment()





if __name__ == '__main__':
    with open('config.json') as config_file:
        data = json.load(config_file)
    bot = WeatherShopper(data)
    bot.run_automation()
