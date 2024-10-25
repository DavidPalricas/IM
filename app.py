import assistant as assi
import tts 

from conextion_config import *
import conextion_config as config

import asyncio

import websockets



HOST = "127.0.0.1:8005"
OUTPUT = "127.0.0.1:8000"

mmi_cli_out = None
send_to_voice = tts.TTS(FusionAdd=f"https://{OUTPUT}/IM/USER1/APPSPEECH").sendToVoice

running = True



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
       while running:
            try:
                message = await websocket.recv()
                
                if message not in ["OK", "RENEW"]:
                    print(message)

                
            except Exception as e:
                print(e)
          


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())