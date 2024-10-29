from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class Video:
    """
    The class Video is responsible for handling events related to a video on YouTube.
    The class has the following attributes:
    - is_short: a boolean that indicates if the video is short or not.
    - is_playing: a boolean that indicates if the video is playing or not.
    - speed: a float that represents the speed of the video.
    - driver: a google chrome driver.
    - youtube: an instance of the WebElement class(body) that represents the YouTube page.
    """
    def __init__(self,is_short,driver):
        """
         Initializes a new instance of the Video class.

         Args:
            - is_short: a boolean that indicates if the video is short or not.
            - driver: a google chrome driver.
        """
        self.is_short = is_short
        self.is_playing = True
        self.speed = 1
        self.driver = driver
        self.youtube =self.driver.find_element("tag name", "body")

    def handling_play_pause(self,send_to_voice,intent):      
         """
             The method handling_play_pause is responsible for handling the player or pause of a youtube event.
             If the intent is play_video and the video is already playing, the assistant will say that the video is already playing, if is not playing, the assistant will call the play_pause method to play the video.
             If the intent is play_video and the video is already playing, the assistant will say that the video is not playing, if is playing, the assistant will call the play_pause method to pause the video.

             Args:
                - send_to_voice: a function that sends a message to the user.
                - intent: a string that represents the intent's name of the user.
         """
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
        """
            The method play_pause is responsible for playing or pausing a video on YouTube and updates the status of the video.
            The method also sends a message to the user to inform is  action.

            Args:
                - send_to_voice: a function that sends a message to the user.
                - play: a boolean that indicates if it is to play the video or not.
        """                 
        if play:
            send_to_voice("Reproduzindo o vídeo")

        else:
            send_to_voice("Pausando o vídeo")
        
        self.youtube.send_keys('k')

        self.is_playing = not self.is_playing

    def change_speed(self,send_to_voice,intent):
        """
            The method change_speed is responsible for changing the speed of a video on YouTube.
            If the video is not playing, the assistant will inform the user that the video is paused and it is not possible to change the speed.
            If the intent is increase_speed_default, the assistant will call the increase_speed method to increase the speed of the video.
            If the intent is decrease_speed_default, the assistant will call the decrease_speed method to decrease the speed of the video.

            Args:
                - send_to_voice: a function that sends a message to the user.
                - intent: a string that represents the intent's name of the user.
            """
        
        if not self.is_playing:
            send_to_voice("O vídeo está pausado, não é possível alterar a velocidade")
            return
         
        key_combination = ActionChains(self.driver)

        if intent == "increase_speed_default":
            self.increase_speed(send_to_voice,key_combination)

        else:
            self.decrease_speed(send_to_voice,key_combination)

    def increase_speed(self,send_to_voice,key_combination):
        """
            The method increase_speed is responsible for increasing the speed of a video on YouTube.
            If the speed is already at the maximum, the assistant will inform the user that the speed is already at the maximum.
            The method increases the speed by 0.25x and sends a message to the user informing the current speed.

            Args:
                - send_to_voice: a function that sends a message to the user.
                - key_combination: an instance of the ActionChains class which represents the keys pressed by the user.
            """
        if self.speed == 2:
            send_to_voice("A velocidade já está no máximo")
            return
              
        self.speed += 0.25
        send_to_voice(f"Aumentando a velocidade em 0.25x, a velocidade atual é de {self.speed}")
        key_combination.key_down(Keys.SHIFT).send_keys('.').key_up(Keys.SHIFT).perform()

    def decrease_speed(self,send_to_voice,key_combination):
        """
            The method decrease_speed is responsible for decreasing the speed of a video on YouTube.
            If the speed is already at the minimum, the assistant will inform the user that the speed is already at the minimum.
            The method decreases the speed by 0.25x and sends a message to the user informing the current speed.

            Args:
                - send_to_voice: a function that sends a message to the user.
                - key_combination: an instance of the ActionChains class which represents the keys pressed by the user.    
        """
        if self.speed == 0.25:
            send_to_voice("A velocidade já está no mínimo")
            return 
        
        self.speed -= 0.25
        send_to_voice(f"Diminuindo a velocidade em 0.25x, a velocidade atual é de {self.speed}")
        key_combination.key_down(Keys.SHIFT).send_keys(',').key_up(Keys.SHIFT).perform()
