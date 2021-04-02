# Speech-Emotion-Recognition

Speech Emotion Recognition from Microphone.

Requirements Installation:
  1. Move to root folder of the project in the command prompt.
  2. Run the followig command : $ pip install -r requirements.txt
  3. All the project necessary libraries will be installed.

Running Project:
  1. Move to root folder of the project in the command prompt.
  2. Run the followig command :
    1. python manage.py makemigrations
    2. python manage.py migrate
    3. python manage.py createsuperuser
    4. python manage.py runserver
  3. Open the browser and run server address.

Note:
  1. Accessing database can be done on browser by moving to /admin address.
  2. The server should run on the microphone enabled machine as the prediction is done using server machine microphone data.
  3. Current model is created using ravdess-data.
  4. The custom audio files and models can be made and can be linked with the main project (Add your custom model as model in static folder).
  5. Link for custom file and model creation project : https://github.com/sarthik126/Audio-and-Model-Maker

Project Description:
  This project is based o machine learning and used for continuous prediction of emotions from the audio extracted from the microphone.
  Accuracy can be increased using best model created using proper and more audios.
  
