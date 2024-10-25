import assistant as assi
import websocket


HOST = "127.0.0.1:8005/IM/USER1/APP1"


#assi = assi.Assistant()


# Funções de manipulador de eventos
def im1_message_handler(ws, message):
    print("Mensagem recebida:", message)

def socket_open_handler(ws):
    print("Conexão aberta")

# Criar conexão com WebSocket
mmiCli_Out = websocket.WebSocketApp(
    HOST,
    on_message=im1_message_handler,
    on_open=socket_open_handler
)


def main():
    mmiCli_Out.send("Hello World")


mmiCli_Out.run_forever()

if __name__ == "__main__":
    main()

#VOICE_MODALITY = "127.0.01.8000"
