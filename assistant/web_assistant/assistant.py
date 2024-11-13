import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from web_app_conextions_files.tts import TTS
from web_assistant.web_assistant import WebAssistant
from consts import OUTPUT
from video import Video
import time

class Assistant(WebAssistant):
    """
      The Assistant class is responsible for handling the assistant's actions and interactions with the user.
      The class has the following attributes:
        - tts: an instance of the TTS class.
        - driver: a google chrome driver.
        - video: an instance of the Video class.
        - running: a boolean that indicates if the assistant is running or not.
    """
    def __init__(self): 
        """
          Initializes a new instance of the Assistant class, and initializes the TTS class and initializes the chrome driver by calling the chrome_config. 
          The construcotr calls the initialize_assistant method.
        """
        self.tts = TTS(FusionAdd=f"https://{OUTPUT}/IM/USER1/APPSPEECH")
        self.send_to_voice("Iniciando o  assistente, aguarde um pouco")
        super().__init__()
        self.driver = self.chrome_config()
        self.video = False
        self.running = True
        self.wait = WebDriverWait(self.driver, 5)

        self.initialize_assistant()
      
    def chrome_config(self):
       """ The chrome_config method is responsible for configuring the chrome options.
          The method will add the user data directory and the profile directory to the chrome options.
         Returns:
              - An instance of the WebDriver class which repsents a chorme driver.
       """
       chrome_options = Options()
       
       # This line is equivalant to this : C:\Users\{user}\AppData\Local\Google\Chrome\User Data
       user_data_dir = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data")

       chrome_options.add_argument(f"user-data-dir={user_data_dir}")

       profile_directory = "Default"

       chrome_options.add_argument(f"--profile-directory={profile_directory}")
       #chrome_options.add_argument("--disable-extensions")
    
       return webdriver.Chrome(options=chrome_options)
    
    def initialize_assistant(self):
        """
        The initialize_assistant method is responsible for initializing the assistant by opening the browser and sending a message to the user.
        """
        self.open("https://www.youtube.com")
        self.send_to_voice("Olá, como posso te ajudar?")

                  
    def send_to_voice(self, message):
        """
        The send_to_voice method is responsible for sending a message to the user using the TTS class's sendo_voice method.
        """
        self.tts.sendToVoice(message) 

    def open(self, url) :
        """
        The open method is responsible for opening a URL in the browser, accepting the cookies by calling the 
         accept_cookies method and maximizing the window.

         Args:
            - url: a string that represents the URL to be opened.
        """
        self.driver.get(url)
        self.driver.maximize_window()
        self.accept_cookies()
        self.load_page()

    def accept_cookies(self):
        """
        The accept_cookies method is responsible for accepting the cookies on the page.
        """
        try:
            # Identify and click the button to accept cookies using text content or classes
            accept_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(text(), 'Aceitar tudo')] or .//span[contains(text(), 'Accept all')]]")
            ))
            accept_button.click()
        except Exception as e:
            print(f"Cookie accept button not found or couldn't be clicked: {e}")
    
    def handling_search_message(self, query):
        """
        The handling_search_message method is responsible for handling the search message.
        If the query contains the word "vídeo" or "vídeos", the method will remove the word from the query.
        And send a message to the user informing that the assistant is searching for the video.

        Args:
            - query: a string that represents the video to be searched.
        """
        if "vídeo" in query:
            query = query.replace("vídeo", "")  

        elif "vídeos" in query:
            query = query.replace("vídeos", "")  
            self.send_to_voice(f"Pesquisando por vídeos {query}")
            return 
        
        self.send_to_voice(f"Pesquisando pelo vídeo {query}")

    def search(self, query) : 
        """
        The search method is responsible for searching for a video on YouTube.
        This method will call the handling_search_message method to handle the search message, after that, the method will open the YouTube page and search for the video.
         will search for the video and click on the first video that is not a sponsered video.
        The method will create a new instance of the Video class and assign it to the video attribute and updates the is_short attribute of the video, if the video is a short video.

        Args:
            - query: a string that represents the video to be searched.
       """
        self.handling_search_message(query)

        visible = EC.visibility_of_element_located
        self.driver.get('https://www.youtube.com/results?search_query={}'.format(str(query)))
    
        self.wait.until(visible((By.ID, "video-title")))

        videos = self.driver.find_elements(By.ID, "video-title") 

        for video in videos:
           if "promoted" not in video.get_attribute("class"):  
               video.click()  

               if "shorts" in  self.driver.current_url:
                   self.video = Video(True,self.driver)
                   break
                
               self.video = Video(False,self.driver)
               self.video.url = self.driver.current_url
               break  

    def shutdown(self) :
        """
        The shutdown method is responsible for shutting down the assistant.
        Before shutting down the assistant, the method will send a message to the user informing that the assistant is shutting down.
        """
        self.send_to_voice("Adeus, espero ter o ajudado")
        self.running = False  
        print("Shutting down assistant...")

        # To check if the user by mistake closes the browser, otherwise the browser will be closed
        if self.driver:
            self.driver.quit()  

    def load_page(self):
        """
        The load_page method is responsible for waiting for the page to load.
        """
        time.sleep(3)

    def write_comment(self, comment):
        """
        The write_comment method is responsible for calling the right method to  write a comment on a YouTube video, and warning the user that the assistant is writing the comment.
        If the video is a short video, the method will call the write_comment_short_video method otherwise it will call the write_comment_long_video method.
    
        Args:
            - comment: a string that represents the comment to be written.
        """

        self.send_to_voice(f"Escrevendo o comentário {comment}")

        if self.video.is_short:
            self.write_comment_short_video(comment)

        else:
            self.write_comment_long_video(comment)
        
    
    def write_comment_short_video(self, comment):
        """
        The write_comment_short_video method is responsible for writing a comment on a short video.
        The method will click on the comment button, and try to find the comment box, if the comment box is not found, the method will send a message to the user informing that the comment box was not found or the comments are disabled.
        Otherwise, the find_comment_box method will be called to write the comment.

        Args:
            - comment: a string that represents the comment to be written.
   
        """

        comment_button = self.driver.find_element(By.ID, "comments-button")
        comment_button.click()
       
        # Time to the comment box to load
        time.sleep(3)

        try:
            self.find_comment_box(comment)

        except NoSuchElementException:
            self.send_to_voice("Erro ao escrever o comentário, a caixa de comentários não foi encontrada ou os comentários estão desativados")


    def write_comment_long_video(self, comment):
        """
        The write_comment_long_video method is responsible for writing a comment on a long video.
        The method will scroll down the yotube page to find the comment box, if the comment box is not found, the method will send a message to the user informing that the comment box was not found or the comments are disabled.
        Otherwise, the find_comment_box method will be called to write the comment.
        In the end, the method will scroll to the beginning of the page.

        Args:
            - comment: a string that represents the comment to be written. 
        """

        scroll_to_comments = 0

        while True:
            # To give time to the comment box to load
            time.sleep(3)
            
            try:
                self.find_comment_box(comment)
                 
                # Time to the user to see the comment
                time.sleep(5)

                break

            except NoSuchElementException: 
                scroll_to_comments += 500
                self.driver.execute_script(f"window.scrollTo(0,{scroll_to_comments});")

                if scroll_to_comments > 1500:
                    self.send_to_voice("Erro ao escrever o comentário, a caixa de comentários não foi encontrada ou os comentários estão desativados")
                    break

        # Scroll to the beginning of the page
        self.driver.execute_script("window.scrollTo(0,0);")

             
    def find_comment_box(self, comment):
        """
        The find_comment_box method is responsible for finding the comment box, clicking on it, and writing the comment in this box.
    
        After that, the method will send a message to the user informing that the comment was written successfully.

        Args:
            - comment: a string that represents the comment to be written.

        """

        comment_box = self.driver.find_element(By.ID, "simplebox-placeholder")

        comment_box.click()

        add_comment_box = self.driver.find_element(By.ID, "contenteditable-root")

        add_comment_box.send_keys(comment)
        
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()
            
        self.send_to_voice("Comentário escrito com sucesso")


    def save_to_playlist(self, playlist):
        """The save_to_playlist method is responsible for trying to save a video into a playlist.
           This methods starts to inform the user that the video is being saved in the playlist.
           The method will call the find_save_option method to find the save option, and the playlist to save the video.
           If the save option is not found, the method will send a message to the user informing that the save option was not found.

            Args:
                - playlist: a string that represents the name of the  playlist to save the video.
        """
        
        self.send_to_voice(f"Guardando o vídeo na playlist {playlist}")

        try:
    
            self.find_save_option(playlist)
           
        except NoSuchElementException:
            self.send_to_voice("Erro ao guardar o vídeo na playlist, o botão para guardar o vídeo não foi encontrado")
        
    def find_save_option(self, playlist):
        """
            The find_save_option method is responsible for finding the save option and the playlist to save the video.
            After the save option is found, the method will store the playlists names ands its checkboxes in a list, and  call the playlist_exits method to check if the searched playlist exists.
            If the searched playlist does not exist, the method will send a message to the user informing that the playlist was not found.
            In the end, the method will call the close_playlist_menu method to close the playlist menu.

            Args:
                - playlist: a string that represents the name of the playlist to save the video.   
        """

        more_options = self.driver.find_element(By.XPATH, '//*[@id="button-shape"]/button')

        more_options.click()

        save_option = self.driver.find_element(By.XPATH, '//*[@id="items"]/ytd-menu-service-item-renderer[2]')

        save_option.click()

        time.sleep(2)

        playlists_container = self.driver.find_elements(By.XPATH, '//ytd-playlist-add-to-option-renderer//tp-yt-paper-checkbox[@id="checkbox"]')

        if not (self.playlist_exits(playlists_container, playlist)):
             self.send_to_voice(f"Erro ao guardar o vídeo na playlist, a playlist {playlist} não foi encontrada")

        time.sleep(2)

        self.close_playlist_menu()

    def playlist_exits(self, playlists_container, playlist):
       """
         The playlist_exits method is responsible for checking if the playlist exists.
         The method will iterate over the playlists founded and check if the searched playlist name matches for any playlist.
         If the playlist is found, the method will click on the playlist checkbox and send a message to the user informing that the video was saved in the playlist.

         Args:
            - playlists_container: a list that contains the container of the playlists(names and checkboxes).
            - playlist: a string that represents the name of the playlist to save the video.

        Returns:
            - True if the playlist was found, otherwise False.
       """

       for playlist_container in playlists_container:
            playlist_name = playlist_container.find_element(By.XPATH, './/yt-formatted-string[@id="label"]').text.lower()

            if playlist_name == playlist.lower():
                playlist_container.click()
                self.send_to_voice("Vídeo guardado na playlist com sucesso")
                return True
            
       return False
    

    def close_playlist_menu(self):
        """
        The close_playlist_menu method is responsible for closing the playlist menu.
        The method will try to find the close palylist menu button in two different languages(english and portuguese), if the button is found, the method will click on it.
        Otherwise, the method will send a message to the user informing that there was an error closing the menu, and refresh the page.

        """
        try:
            close_menu = self.driver.find_element(By.XPATH, '//*[@id="button" and @aria-label="Cancel"]')

        except NoSuchElementException:
            try:    
                close_menu = self.driver.find_element(By.XPATH, '//*[@id="button" and @aria-label="Cancelar"]')

            except NoSuchElementException:
                close_menu = None  

        if close_menu:
            close_menu.click()
        else:
            self.send_to_voice("Erro ao fechar o menu de opções, dando refresh na página")
            self.driver.refresh()
                   
    def execute_action(self, nlu):
        """
        The execute_action method is responsible for executing the action based on the user's intent.

        Args:
            - nlu: a dictionary that contains the intent and entities of the user's message.
        """
        match nlu["intent"]:
            case "search_video":
                self.search(nlu["entities"])

            case "shutdown_assistant":
                self.shutdown()

            case "pause_video" | "play_video":
                if self.video == None:
                    self.send_to_voice("Não há nenhum vídeo para pausar")
                else:
                   self.video.handling_play_pause(self.send_to_voice,nlu["intent"])

            case "increase_speed" | "decrease_speed":
                if self.video == None:
                    self.send_to_voice("Não há nenhum vídeo para alterar a velocidade")
                else:
                    self.video.change_speed(self.send_to_voice,nlu["intent"])
            
            case "write_comment":
                if self.video == None:
                    self.send_to_voice("Não há nenhum vídeo para comentar")
                else:
                    self.write_comment(nlu["entities"])

            case "activate_video_subtitles" | "deactivate_video_subtitles":
                if self.video == None:
                    self.send_to_voice("Não há nenhum vídeo para ativar ou desativar as legendas")
                else:
                    self.video.on_off_video_subtitles(self.send_to_voice,nlu["intent"])
            
            case "mute_video" | "unmute_video":
                if self.video == None:
                    self.send_to_voice("Não há nenhum vídeo para ativar ou desativar o som")
                else:
                    self.video.mute_unmute_video(self.send_to_voice,nlu["intent"])

            case "seek_forward_video" | "seek_backward_video":
                if self.video == None:
                    self.send_to_voice("Não há nenhum vídeo para avançar ou retroceder")
                else:
                    video_url = self.video.seek_forward_backward(self.send_to_voice,nlu["intent"], nlu["entities"])

                    if video_url != None:
                        self.open(video_url)
                        self.video.youtube = self.driver.find_element("tag name", "body")

            case "save_to_playlist":
                if self.video == None:
                    self.send_to_voice("Não há nenhum vídeo para salvar na playlist")
                else:
                    self.save_to_playlist(nlu["entities"])
                        
            case _:
                self.send_to_voice("Desculpe, não entendi o que você disse")

                


            

      