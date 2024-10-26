# IM

# How to run
 ## First Step
  Open a `terminal` in this directory and start the `mmiframework` with this commands:
   ```ps
   cd .\mmiframework2\; ./start.bat
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

  ## Last Step
   To run our `assistant` open a `terminal` in this folder and execute the next command
   ```ps
   cd ./assistant/; ./app.bat
   ```