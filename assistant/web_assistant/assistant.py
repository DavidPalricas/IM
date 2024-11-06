import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
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
        The write_comment method is responsible for writing a comment on a YouTube video.
        The method will scroll the page to the comment box, click on the comment box, write the comment and send the comment by pressing the control key plus the enter key.
        After sending the comment, the method will send a message to the user informing that the comment was written successfully.

        Args:
            - comment: a string that represents the comment to be written.
        """

        self.send_to_voice(f"Escrevendo o comentário {comment}")

        self.load_page()

        try:
    
            add_comment = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='simplebox-placeholder']")))
            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", add_comment)

            ActionChains(self.driver).move_to_element(add_comment).click().perform()

            self.load_page()

      
            comment_input = self.driver.find_element(By.XPATH, "//*[@id='contenteditable-root']")
            comment_input.send_keys(comment)
            comment_input.send_keys(Keys.CONTROL, Keys.ENTER)

            self.load_page()

            self.send_to_voice("Comentário escrito com sucesso")
            
        except Exception as e:
            self.send_to_voice("Erro ao tentar escrever o comentário")
            print(f"Erro: {e}")

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

            case "increase_speed_default" | "decrease_speed_default":
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
                        

            case _:
                self.send_to_voice("Desculpe, não entendi o que você disse")

                


            

      