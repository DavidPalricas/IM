# IM

# Requirements
* Windows Operative System
* Python 3.10 or greater
* Java 21
* Node JS
* Miniconda 3

Execute the following command to install all the python ibraries requirements
```ps
pip install -r requirements.txt
```
# How to run
 ## First Step
  Open a `terminal` in this directory and start the `mmiframework` with this commands:
   ```ps
   cd .\mmiframeworkV2\; ./start.bat
   ```

   ## Second Step
   Open another `terminal` in this directory and star the `Fusion Engine` with the following command:
   ```ps
   cd .\FusionEngine\; ./start.bat
   ``` 

   ## Third Step
   Open a `Anacond Prompt (Miniconda3)` and execute this command:
   ```bat
    activate rasa-env &&  cd .\rasa\
  ```

  If it is your `first` time running this project or you made `any change` of a file in the `rasa folder`, before tou start the `rasa server` you need to execute the following command to generate a new `rasa model`
  ```bat
  rasa train
  ```
  Otherwise you can run this command, to start the `rasa server`
  ```
  rasa run --enable-api -m .\models\ --cors "*"
  ```

  ## Fourth Step
  To start the `web app server` open a `terminal` in this folder and execute the following command
  ````ps
   cd .\WebAppAssistantV2\;   ./start_web_app.bat
  ````

  ## Fifth Step
   To run our `assistant` open a `terminal` in this folder and execute the next command
   ```ps
   cd ./assistant/; ./app.bat
   ```

  ## Last Step
   Ensure your chrome profile is set in the directory `C:\Users\{user}\AppData\Local\Google\Chrome\User Data\Default`. 
   To check this path open the google chrome and write `chrome://version/`, like in the picture below

   ![Chrome Profile Path](img/chrome_profile_path.png)

   After that make sure your `google account` is logged in `youtube`.

  ## Optional Step
    In case the last step didn't work, when you run "cd ./assistant/; ./app.bat" you maybe saw a message like this:
    ```
    (session not created: DevToolsActivePort file doesn't exist)
    (The process started from chrome location C:\Program Files (x86)\Google\Chrome\Application\chrome.exe is no longer running, so ChromeDriver is assuming that Chrome has crashed.) 
  Stacktrace: ...
              ...
    [19312:12548:1031/232204.442:ERROR:command_buffer_proxy_impl.cc(324)] GPU state invalid after WaitForGetOffsetInRange.
    ```
    Try to run the following command in the terminal:
    ```ps
      taskkill /F /IM chrome.exe /T
    ```
    And then run the assistant again.
    This command will kill all the chrome processes running in the background. We need to do this or the assistant will not work properly.