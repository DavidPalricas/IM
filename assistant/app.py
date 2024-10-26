import assistant.assistant as assi
import assistant.web_app_conextions_files.tts as tts 
import json
import xml.etree.ElementTree as ET

from web_app_conextions_files.conextion_config import *


import asyncio

import websockets



HOST = "127.0.0.1:8005"
OUTPUT = "127.0.0.1:8000"

mmi_cli_out = None
send_to_voice = tts.TTS(FusionAdd=f"https://{OUTPUT}/IM/USER1/APPSPEECH").sendToVoice

running = True



def nlu_extrator(message):
  """
  Extracts the nlu from the websocket's message
  Parameters: message (str): The message received from the websocket
  """ 
   # Remove the <comand> tag
  comand_tag = ET.fromstring(message).findall(".//command")
   
   # Removes the text from the comand tag and converts it to a json
  message = json.loads(comand_tag.pop(0).text)
 
  return {"text": message["text"],"intent":message["intent"]["name"],"entities":message["entities"]}



async def main():


    mmi_cli_out_Add = f"wss://{HOST}/IM/USER1/APP"

    ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
   # mmi_cli_out =  config.MMIClientSocket(mmi_cli_out_Add + "APP")
    #mmi_cli_out.onMessage.on(message_handler)
    #mmi_cli_out.onOpen.on(socket_open_handler)
    #await mmi_cli_out.openSocket()


    async with websockets.connect( mmi_cli_out_Add,ssl = ssl_context) as websocket:
       print("connected Websocket")
       #tts.TTS(FusionAdd=f"https://{OUTPUT}/IM/USER1/SPEECH").sendToVoice("boas")

       while running:
            try:
                print("waiting message")
                message = await websocket.recv()
                
                if message not in ["OK","RENEW"]:
                      
                      nlu = nlu_extrator(message)

                      print(nlu)

                      
            except Exception as e:
                            print(e)
                    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())