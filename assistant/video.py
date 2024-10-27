from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Video:
    def __init__(self,is_short):
        self.is_short = is_short
        self.is_playing = True

    def handling_play_pause(self,driver,send_to_voice,intent):
         if self.is_playing :
            if intent == "play_video":
                send_to_voice("O vídeo já está sendo reproduzido")
            else:
                self.play_pause(driver,send_to_voice,False)
         else:
            if intent == "pause_video":
                send_to_voice("O vídeo já está pausado")
            else:
                self.play_pause(driver,send_to_voice,intent)

    def play_pause(self,driver,send_to_voice,play):                 
        if play:
            send_to_voice("Reproduzindo o vídeo")

        else:
            send_to_voice("Pausando o vídeo")

        if self.is_short:
            play_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Reproduzir (k)' or @aria-label='Play (k)']"))
            )
        else:   
            play_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".ytp-play-button"))
            )
            play_button.click()  

        self.is_playing = not self.is_playing

