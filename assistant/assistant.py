from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_app_conextions_files.tts import TTS
from consts import OUTPUT
from video import Video
import time

class Assistant:
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
          Initializes a new instance of the Assistant class.
          And calls the initialize_assistant method.
        """
        self.tts = TTS(FusionAdd=f"https://{OUTPUT}/IM/USER1/APPSPEECH")
        self.driver = webdriver.Chrome()
        self.video = False
        self.running = True

        self.initialize_assistant()
      
    def initialize_assistant(self):
        """
        The initialize_assistant method is responsible for initializing the assistant by opening the browser and sending a message to the user.
        """
        self.open("https://www.youtube.com")
        self.send_to_voice("Olá, como posso ajudar?")
           
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
            wait = WebDriverWait(self.driver, 5)
            # Identify and click the button to accept cookies using text content or classes
            accept_button = wait.until(EC.element_to_be_clickable(
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

        wait = WebDriverWait(self.driver, 3)
        visible = EC.visibility_of_element_located
        self.driver.get('https://www.youtube.com/results?search_query={}'.format(str(query)))
    
        wait.until(visible((By.ID, "video-title")))

        videos = self.driver.find_elements(By.ID, "video-title") 

        for video in videos:
           # Verificar se o vídeo não é um anúncio
           if "promoted" not in video.get_attribute("class"):  # Assumindo que anúncios contêm 'ad' na classe
               video.click()  # Clicar no primeiro vídeo que não é um anúncio

               if "shorts" in  self.driver.current_url:
                   self.video = Video(True,self.driver)
                   break
                
               self.video = Video(False,self.driver)
               break  # Sai


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
        time.sleep(5)

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

                


            

      