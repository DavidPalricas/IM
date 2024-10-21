from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Assistant:
    def __init__(self) : 
        self.driver = webdriver.Chrome()
        self.search_bar = None 

    def open(self, url) :
        self.driver.get(url)

        self.search_bar = self.driver.find_element("class name", "gLFyf")

        self.load_page()

    def search(self, query) :
        self.search_bar.send_keys(query)

        #Enter key
        self.search_bar.send_keys(Keys.RETURN)
        
        self.load_page()

    def close(self) :
        self.driver.quit()

    def load_page(self):
         # To wait for the page to load
        time.sleep(5)