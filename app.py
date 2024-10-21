import assistant as assi
import keyboard as key
def main():

    assistant = assi.Assistant()
    assistant.open("https://www.google.com")
    
    running = True
    while running:
        if key.is_pressed("q"):
            assistant.close()
            running = False
        elif key.is_pressed("s"):
            assistant.search("Vintage Cars")
    
    

if __name__ == "__main__":
    main()