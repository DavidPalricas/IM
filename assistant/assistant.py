from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class Assistant:
    def __init__(self) : 
        self.driver = webdriver.Chrome()
        self.search_bar = None 

    def open(self, url) :
        self.driver.get(url)
        self.driver.maximize_window()

        self.load_page()

    def search(self, query) :        
        wait = WebDriverWait(self.driver, 3)
        visible = EC.visibility_of_element_located
        self.driver.get('https://www.youtube.com/results?search_query={}'.format(str(query)))
    

        wait.until(visible((By.ID, "video-title")))
        self.driver.find_element(By.ID, "video-title").click()

    def close(self) :
        self.driver.quit()

    def load_page(self):
         # To wait for the page to load
        time.sleep(5)