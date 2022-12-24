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
        s = Service('/Users/swaggy/Downloads/chromedriver 2')
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
        self.driver.get('https://weathershopper.pythonanywhere.com/moisturizer')

    def get_aloe(self):
        """Get cheapest aloe and parse"""
        self.current_aloe = []
        aloes = self.driver.find_elements(By.XPATH, "//*[contains(text(),'Aloe') or \
               contains(text(),'aloe')]/following-sibling::p")

        for aloe in aloes:
            for cheapest_aloe in aloe.text.split():
                if cheapest_aloe.isdigit():
                    self.current_aloe.append(cheapest_aloe)
                    self.current_aloe.sort()

        self.driver.find_element(By.XPATH, "//*[contains(text(),'Aloe') or \
               contains(text(),'aloe')]/following-sibling::p[contains(text(),%s)]/following-sibling::\
                   button[text() = 'Add']" % self.current_aloe[0]).click()

        print("Currently the cheapest Aloe moisturizer is priced at: " + self.current_aloe[0] + " rupees")

    def get_almond(self):
        """Get cheapest almond moisturizer and parse"""
        self.current_almond = []
        almonds = self.driver.find_elements(By.XPATH, "//*[contains(text(),'Almond') or \
                       contains(text(),'almond')]/following-sibling::p")

        for almond in almonds:
            for cheapest_almond in almond.text.split():
                if cheapest_almond.isdigit():
                    self.current_almond.append(cheapest_almond)
                    self.current_almond.sort()

        self.driver.find_element(By.XPATH, "//*[contains(text(),'Almond') or \
                       contains(text(),'almond')]/following-sibling::p[contains(text(),%s)]/following-sibling::\
                           button[text() = 'Add']" % self.current_almond[0]).click()

        print("Currently the cheapest Almond moisturizer is priced at: " + self.current_almond[0] + " rupees")

    def cart_click_and_purchase_moisturizer(self):
        """Verify lotions and purchase"""
        self.driver.find_element(By.CLASS_NAME, 'thin-text.nav-link').click()
        cheapest_moisturizers = []
        moisturizers = self.driver.find_elements(By.XPATH, "//*[contains(text(),'Aloe') or \
                contains(text(),'aloe') or contains(text(),'Almond') or contains(text(),'almond')]/following-sibling::td")

        for moisturizer in moisturizers:
            current_moisturizer = moisturizer.text
            cheapest_moisturizers.append(current_moisturizer)

        if self.current_aloe[0] and self.current_almond[0] in cheapest_moisturizers:
            print("Processing your order for both moisturizer lotions now.")
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/button/span').click()
        else:
            print('Failed')

    def get_spf_30(self):
        """Get cheapest SPF-30 price and parse"""
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

        print("Currently the cheapest SPF-30 sunscreen is priced at: " + self.current_spf_30[0] + " rupees")

    def get_spf_50(self):
        """Get Cheapest SPF-50 price and parse"""
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
        print("Currently the cheapest SPF-50 sunscreen is priced at: " + self.current_spf_50[0] + " rupees")


    def cart_click_and_purchase_sunscreen(self):
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
        """Within the iFrame, input card information from Stripe"""
        self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME,'iframe'))

        wait = WebDriverWait(self.driver, 20)
        email = wait.until(EC.element_to_be_clickable((By.ID, 'email')))
        email.send_keys(self.email)

        card_number = wait.until(EC.element_to_be_clickable((By.ID, 'card_number')))
        for delay in self.card_number:
            card_number.send_keys(delay)
            time.sleep(.1)

        card_year = wait.until(EC.element_to_be_clickable((By.ID, 'cc-exp')))
        for delay in self.card_year:
            card_year.send_keys(delay)
            time.sleep(.1)

        card_cvc = wait.until(EC.element_to_be_clickable((By.ID, 'cc-csc')))
        card_cvc.send_keys(self.cvc)

        zipcode = wait.until(EC.element_to_be_clickable((By.ID, 'billing-zip')))
        zipcode.send_keys(self.zipcode)

        self.driver.find_element(By.CLASS_NAME, 'iconTick').click()
        self.driver.switch_to.default_content()
        print('Purchase Successful!')

    def dynamic_automate(self):
        """Weather decides if we need sunscreens or moisturizers!"""
        sunscreens = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/h2').text
        if sunscreens == 'Sunscreens':
            print("Treat your skin right. Don't leave your home without your favorite sunscreen. Say goodbye to sunburns.")
            self.sunscreen_automate()
        else:
            print("Don't let cold weather ruin your skin. Use your favourite moisturizer and keep your skin stay young.")
            self.moisturizer_automate()


    def moisturizer_automate(self):
        """Cold days we need to moisturize!"""
        self.get_aloe()
        self.get_almond()
        self.cart_click_and_purchase_moisturizer()

    def sunscreen_automate(self):
        """Sunny days we get sunscreen!"""
        self.get_spf_30()
        self.get_spf_50()
        self.cart_click_and_purchase_sunscreen()

    def run_automation(self):
        """Dynamic functions to run our automation test"""
        self.start_website()
        self.get_current_temp()
        self.dynamic_automate()
        self.card_payment()

if __name__ == '__main__':
    with open('config.json') as config_file:
        data = json.load(config_file)
    bot = WeatherShopper(data)
    bot.run_automation()
