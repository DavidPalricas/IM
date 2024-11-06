from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


class Video:
    """
    The class Video is responsible for handling events related to a video on YouTube.
    The class has the following attributes:
    - is_short: a boolean that indicates if the video is short or not.
    - is_playing: a boolean that indicates if the video is playing or not.
    - speed: a float that represents the speed of the video.
    - driver: an instance of the WebDriver class.
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
        self.subtitles = False
        self.muted = False
        self.speed = 1
        self.driver = driver
        self.youtube =self.driver.find_element("tag name", "body")


    def get_video_time(self):
        """
        Retrieves the current time and total duration of the YouTube video.
        
        Returns:
            tuple: A tuple containing the current time and total duration as strings.
        """
        try:
            # Locate the elements containing the current and total time
            print("ggllglgllglgllglglgllglg")
            # Pause video first
            if self.is_playing:
                self.youtube.send_keys('k')

            current_time_element = self.driver.find_element(By.CLASS_NAME, 'ytp-time-current')
            total_time_element = self.driver.find_element(By.CLASS_NAME, 'ytp-time-duration')
            print(f"current_time_element: {current_time_element}, total_time_element: {total_time_element}")

            # Extract the text (time) from the elements
            current_time = current_time_element.text
            total_time = total_time_element.text
            print(f"current_time: {current_time}, total_time: {total_time}")

            # Play video again
            self.youtube.send_keys('k')
            # Print or return the time values
            return current_time, total_time
        
        except Exception as e:
            print(f"Error while retrieving video times: {e}")
            return None, None


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

    def on_off_video_subtitles(self,send_to_voice,intent):
        """
            The method on_off_video_subtitles is responsible for turning on or off the subtitles of a video on YouTube.
            If the intent is turn_on_subtitles, the assistant will call the turn_on_subtitles method to turn on the subtitles.
            If the intent is turn_off_subtitles, the assistant will call the turn_off_subtitles method to turn off the subtitles.

            Args:
                - send_to_voice: a function that sends a message to the user.
                - intent: a string that represents the intent's name of the user.
        """
        if self.subtitles:
            if intent == "activate_video_subtitles":
                send_to_voice("As legendas já estão ativadas")
            else:
                self.turn_on_off_subtitles(send_to_voice,False)
        else:
            if intent == "deactivate_video_subtitles":
                send_to_voice("As legendas já estão desativadas")
            else:
                self.turn_on_off_subtitles(send_to_voice,True)

    def turn_on_off_subtitles(self,send_to_voice,turn_on):
        """
            The method turn_on_off_subtitles is responsible for turning on or off the subtitles of a video on YouTube.
            The method also sends a message to the user to inform the action.

            Args:
                - send_to_voice: a function that sends a message to the user.
                - turn_on: a boolean that indicates if it is to turn on the subtitles or not.
        """
        if turn_on:
            send_to_voice("Ativando as legendas")
        else:
            send_to_voice("Desativando as legendas")

        self.youtube.send_keys('c')
        self.subtitles = not self.subtitles

    def mute_unmute_video(self,send_to_voice,intent):
        """
            The method mute_unmute_video is responsible for muting or unmuting a video on YouTube.
            If the intent is mute_video, the assistant will call the mute_unmute method to mute the video.
            If the intent is unmute_video, the assistant will call the mute_unmute method to unmute the video.

            Args:
                - send_to_voice: a function that sends a message to the user.
                - intent: a string that represents the intent's name of the user.
        """
        if self.muted:
            if intent == "mute_video":
                send_to_voice("O vídeo já está mudo")
            else:
                self.mute_unmute(send_to_voice,False)
        else:
            if intent == "unmute_video":
                send_to_voice("O vídeo já está com o som ativado")
            else:
                self.mute_unmute(send_to_voice,True)

    def mute_unmute(self,send_to_voice,mute):
        """
            The method mute_unmute is responsible for muting or unmuting a video on YouTube.
            The method also sends a message to the user to inform the action.

            Args:
                - send_to_voice: a function that sends a message to the user.
                - mute: a boolean that indicates if it is to mute the video or not.
        """
        if mute:
            send_to_voice("Mudando o vídeo")
        else:
            send_to_voice("Ativando o som do vídeo")

        self.youtube.send_keys('m')
        self.muted = not self.muted

    def seek_forward_backward(self,send_to_voice,intent,entities):
        """
            The method seek_forward_backward is responsible for seeking forward or backward a video on YouTube.
            If the intent is seek_forward, the assistant will call the seek method to seek forward the video.
            If the intent is seek_backward, the assistant will call the seek method to seek backward the video.

            Args:
                - send_to_voice: a function that sends a message to the user.
                - intent: a string that represents the intent's name of the user.
                - entities: a dictionary that contains the entities found in the user's message.
        """
        if intent == "seek_forward_video":
            return self.seek(send_to_voice,entities,True)
        else:
            time = entities["time"]
            return self.seek(send_to_voice,entities,False)

    def seek(self,send_to_voice,entities,forward):
        """
            The method seek is responsible for seeking forward or backward a video on YouTube.
            The method also sends a message to the user to inform the action.

            Args:
                - send_to_voice: a function that sends a message to the user.
                - entities: a dictionary that contains the entities found in the user's message.
                - forward: a boolean that indicates if it is to seek forward or backward the video.
        """
        print("eeeeeeeeeeeeeeeeeeeeeeee : "+entities)
        if forward:
            send_to_voice(f"Avançando {entities}")
        else:
            send_to_voice(f"Retrocedendo {entities}")

        time = self.convert_time(entities)
        print("timeeeeeeeeeeeeeeeeeeeeeeeee : "+str(time))
        if time >= 36000: 
            send_to_voice("O tempo é muito grande, não é possível avançar ou retroceder")
            return

        if time <= 90:

            for _ in range(round(time / 10)):
                self.youtube.send_keys('l' if forward else 'j')


        else: 
            return f"{self.driver.current_url}&t={time}s"

        return None



        

    def convert_time(self,entities):
        """
            The method convert_time is responsible for converting the time to seconds.

            Args:
                - time: a string that represents the time.

            Returns:
                - int: the time converted to seconds.
        """

        time_units = ["segundos","minutos","horas"]

        type_time = entities.split(" ")[1]
        time = int(entities.split(" ")[0])

        # get video time in seconds, and add it to the current time
        current_time, total_time = self.get_video_time()
        
        current_time = current_time.split(":")

        time_append = (int(current_time[0]) * 3600 + int(current_time[1]) * 60 + int(current_time[2])) if len(current_time) == 3 else (int(current_time[0]) * 60 + int(current_time[1]))


        for i in range(len(time_units)):
            if type_time == time_units[i] or type_time == time_units[i][:-1]:
                return time * 60 ** i + time_append, total_time
        
        return time, total_time
