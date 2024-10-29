from assistant import Assistant
import json
import xml.etree.ElementTree as ET
from web_app_conextions_files.conextion_config import *
import asyncio
import websockets
from consts import HOST
from web_app_conextions_files.tts import TTS


def nlu_exctrator(message):
  """
  The nlu_exctrator exctracts the nlu from the websocket's message
  
  Args:
    message (str): The message received from the websocket

  Returns:
    dict: The nlu extracted from the message(contains the user's intent and entities found)
  """ 
   # Remove the <comand> tag
  comand_tag = ET.fromstring(message).findall(".//command")
   
   # Removes the text from the comand tag 
  message = json.loads(comand_tag.pop(0).text)

  nlu = json.loads(message["nlu"])

  if nlu["entities"] == []:
    return {"intent": nlu["intent"] ["name"]}
  
  print(nlu["entities"])
  
  return {"intent": nlu["intent"] ["name"], "entities": nlu["entities"][0]["value"]}


def ignore_certificates():
  """
  The ignore_certificates function is responsible for ignoring the web certificates
  """
  ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
  ssl_context.check_hostname = False
  ssl_context.verify_mode = ssl.CERT_NONE

  return ssl_context

async def main():
  """
   The main function is responsible for starting the assistant, and make the conection to the WebApp's websocket
   It also is responsible for receiving messages and calling the nlu_exctrator function to extract the nlu from the message
   After that, the function calls the assistant's execute_action method to execute the action based on the nlu
  """

  assistant = Assistant()

  # Websocket url adress
  mmi_cli_out_Add = f"wss://{HOST}/IM/USER1/APP"
  
  ssl_context = ignore_certificates()

  async with websockets.connect( mmi_cli_out_Add,ssl = ssl_context) as websocket:
      print("Connected Websocket")

      while assistant.running:
          try:
            print("Waiting for messages")
            message = await websocket.recv()
            
            if message not in ["OK","RENEW"]:  
              print(message)   
              nlu = nlu_exctrator(message)
              print("Message received")

              assistant.execute_action(nlu)
                      
          except Exception as e:
                print(e)
                      
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())