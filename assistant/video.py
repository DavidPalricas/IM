from selenium import webdriver
from selenium.webdriver.common.by import By
class Video:
    def __init__(self,is_short):
        self.is_short = is_short
        self.is_playing = True


    def play_pause(self,driver,send_to_voice):
         if self.is_playing:
            send_to_voice("Pausando o vídeo")
            driver.find_element(By.CSS_SELECTOR, ".ytp-play-button").click()
         else:
            send_to_voice("O vídeo já está pausado")
    