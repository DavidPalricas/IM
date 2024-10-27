from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_app_conextions_files.tts import TTS
from consts import OUTPUT
from video import Video
import time

class Assistant:
    def __init__(self): 
        self.tts = TTS(FusionAdd=f"https://{OUTPUT}/IM/USER1/APPSPEECH")
        self.driver = webdriver.Chrome()
        self.open("https://www.youtube.com")
        self.send_to_voice("Olá, como posso ajudar?")
        self.video = False
        self.running = True
           
    def send_to_voice(self, message):
        self.tts.sendToVoice(message) 

    def open(self, url) :
        self.driver.get(url)
        self.driver.maximize_window()
        self.accept_cookies()
        self.load_page()

    def accept_cookies(self):
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
        if "vídeo" in query:
            query = query.replace("vídeo", "")  

        elif "vídeos" in query:
            query = query.replace("vídeos", "")  
            self.send_to_voice(f"Pesquisando por vídeos {query}")
            return 
        
        self.send_to_voice(f"Pesquisando pelo vídeo {query}")

    def search(self, query) : 
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
                   self.video = Video(True)
                   break
                
               self.video = Video(False)
               break  # Sai


    def shutdown(self) :
        self.send_to_voice("Adeus, espero ter o ajudado")
        self.running = False  
        print("Shutting down assistant...")

        # To check if the user by mistake closes the browser, otherwise the browser will be closed
        if self.driver:
            self.driver.quit()  


    def load_page(self):
         # To wait for the page to load
        time.sleep(5)

    def execute_action(self, nlu):
        match nlu["intent"]:
            case "search_video":
                self.search(nlu["entities"])

            case "shutdown_assistant":
                self.shutdown()

            case "pause_video" | "play_video":
                if self.video == None:
                    self.send_to_voice("Não há nenhum vídeo para pausar")
                else:
                   self.video.handling_play_pause(self.driver,self.send_to_voice,nlu["intent"])

                


            

      