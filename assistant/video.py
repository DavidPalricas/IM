from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class Video:
    def __init__(self,is_short,driver):
        self.is_short = is_short
        self.is_playing = True
        self.speed = 1
        self.driver = driver
        self.youtube =self.driver.find_element("tag name", "body")

    def handling_play_pause(self,send_to_voice,intent):
         if self.is_playing :
            if intent == "play_video":
                send_to_voice("O vídeo já está sendo reproduzido")
            else:
                self.play_pause(send_to_voice,False)
         else:
            if intent == "pause_video":
                send_to_voice("O vídeo já está pausado")
            else:
                self.play_pause(send_to_voice,intent)

    def play_pause(self,send_to_voice,play):                 
        if play:
            send_to_voice("Reproduzindo o vídeo")

        else:
            send_to_voice("Pausando o vídeo")
        
        self.youtube.send_keys('k')

        self.is_playing = not self.is_playing


    def change_speed(self,send_to_voice,intent):

        if not self.is_playing:
            send_to_voice("O vídeo está pausado, não é possível alterar a velocidade")
            return
         
        key_combination = ActionChains(self.driver)

        if intent == "increase_speed_default":
            self.increase_speed(send_to_voice,key_combination)

        else:
            self.decrease_speed(send_to_voice,key_combination)

      


    def increase_speed(self,send_to_voice,key_combination):
        if self.speed == 2:
            send_to_voice("A velocidade já está no máximo")
            return
              
        self.speed += 0.25
        send_to_voice(f"Aumentando a velocidade em 0.25x, a velocidade atual é de {self.speed}")
        key_combination.key_down(Keys.SHIFT).send_keys('.').key_up(Keys.SHIFT).perform()



    def decrease_speed(self,send_to_voice,key_combination):
        if self.speed == 0.25:
            send_to_voice("A velocidade já está no mínimo")
            return 
        
        self.speed -= 0.25
        send_to_voice(f"Diminuindo a velocidade em 0.25x, a velocidade atual é de {self.speed}")
        key_combination.key_down(Keys.SHIFT).send_keys(',').key_up(Keys.SHIFT).perform()

        
       

