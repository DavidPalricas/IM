from selenium.webdriver.common.by import By
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
        send_to_voice("Reproduzindo o vídeo") if play else send_to_voice("Pausando o vídeo")
        
        driver.find_element(By.CSS_SELECTOR, ".ytp-play-button").click()
        self.is_playing = not self.is_playing

