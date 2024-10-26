from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_app_conextions_files.tts import TTS
from consts import OUTPUT
import time

class Assistant:
    def __init__(self): 
        self.tts = TTS(FusionAdd=f"https://{OUTPUT}/IM/USER1/APPSPEECH")
        self.driver = webdriver.Chrome()
        self.open("https://www.youtube.com")
        self.send_to_voice("Olá, como posso ajudar?")
        self.video = None
           
    def send_to_voice(self, message):
        self.tts.sendToVoice(message) 

    def open(self, url) :
        self.driver.get(url)
        self.driver.maximize_window()

        self.load_page()

    def search(self, query) :        
        wait = WebDriverWait(self.driver, 3)
        visible = EC.visibility_of_element_located
        self.driver.get('https://www.youtube.com/results?search_query={}'.format(str(query)))
    
        wait.until(visible((By.ID, "video-title")))

        videos = self.driver.find_elements(By.ID, "video-title") 

        for video in videos:
           # Verificar se o vídeo não é um anúncio
           if "promoted" not in video.get_attribute("class"):  # Assumindo que anúncios contêm 'ad' na classe
               video.click()  # Clicar no primeiro vídeo que não é um anúncio
               break  # Sai


    def close(self) :
        self.driver.quit()

    def load_page(self):
         # To wait for the page to load
        time.sleep(5)


    def execute_action(self, nlu):
      match nlu["intent"]:
          case "search_video":
              self.send_to_voice(f"Pesquisando pelo video {nlu['entities']}")
              self.search(nlu["entities"])

          case "shutdown_assistant":
              self.send_to_voice("Adeus, espero ter o ajudado")
              self.close()

            

      