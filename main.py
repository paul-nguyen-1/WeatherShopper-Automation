import json
import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

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
            print('moist')
            print(current_temp)
        else:
            print('sunscreens')
            print(current_temp)
















    def run_automation(self):
        self.start_website()
        self.get_current_temp()
        self.driver.quit()

if __name__ == '__main__':
    with open('config.json') as config_file:
        data = json.load(config_file)
    bot = WeatherShopper(data)
    bot.run_automation()
