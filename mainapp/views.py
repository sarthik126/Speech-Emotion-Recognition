from django.shortcuts import render
from django.urls import reverse_lazy

import threading
from .models import ValueTable

import librosa
import soundfile
import os, glob, pickle
import numpy as np
import sounddevice
from scipy.io.wavfile import write

flag = False

# Create your views here.
class HandleThread(threading.Thread):
	"""docstring for HandleThread"""

	#DataFlair - Extract features (mfcc, chroma, mel) from a sound file
	def extract_feature1(self,file_name, mfcc, chroma, mel):
		with soundfile.SoundFile(file_name) as sound_file:
			X = sound_file.read(dtype="float32")
			sample_rate=sound_file.samplerate
			if chroma:
				stft=np.abs(librosa.stft(X))
			result=np.array([])
			if mfcc:
				mfccs=np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
				result=np.hstack((result, mfccs))
			if chroma:
				chroma=np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
				result=np.hstack((result, chroma))
			if mel:
				mel=np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
				result=np.hstack((result, mel))
			return result


	# DataFlair - Load the data and extract features for each sound file
	def load_data(self,filename):
		x = []
		for file in glob.glob(filename):
			file_name = os.path.basename(file)
			
			#sound = AudioSegment.from_mp3(filename)
			#sound.export(file, format="wav")

			feature = self.extract_feature1(file, mfcc=True, chroma=True, mel=True)
			x.append(feature)
		return x

	def main_function(self):
		filename="static/model1"
		model=pickle.load(open(filename,"rb"))

		fs = 16000
		second = 3

		#print("recording...")

		while True:
			#print("..........")
			record_voice = sounddevice.rec(int(second*fs),samplerate=fs,channels=1)
			sounddevice.wait()
			write("static/output.wav",fs,record_voice)
			x_test1=self.load_data("static/output.wav")
			y_pred1=model.predict(x_test1)

			pred_value = y_pred1.tostring().decode("utf-8")
			
			#Save the predicted value
			obj = ValueTable.objects.create(value1 = pred_value)
			#print(pred_value)

			#print(flag)
			if flag:
				break
		return "Thread Stopped..."

	def __init__(self):
		#self.args = args
		threading.Thread.__init__(self)

	def run(self):
		th = self.main_function()
		print(th)
		#print("thread working...",self.arg)

'''class MainView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['values'] = ValueTable.objects.all()
        #HandleThread("helloo").start()
        return context'''

def main(request):
	'''global flag
	flag = False
	th = HandleThread()
	th.start()'''
	return render(request, "index.html")

def loader(request):
	val = ValueTable.objects.last()
	#print(val.value1)
	context1={"value1":val}
	#HandleThread("helloo").start()
	return render(request,"loader.html",context1)

def stopthread(request):
	global flag
	flag = True
	context1={"value1":"Prediction Stopped..."}
	return render(request, "loader.html",context1)

def starter(request):
	global flag
	flag = False
	th = HandleThread()
	th.start()
	context1={"value1":"Starting Prediction..."}
	return render(request,"loader.html",context1)
