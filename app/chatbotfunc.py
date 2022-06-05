from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from azure_translator import Translator
import requests, uuid, json
from gtts import gTTS 
# from IPython.display import Audio 
import mysql.connector
from mysql.connector import errorcode
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import os
from django.conf import settings

def chat(sp):
	chatbot = ChatBot('corona bot')
	trainer = ChatterBotCorpusTrainer(chatbot)
	trainer.train("chatterbot.corpus.english.greetings",
				"chatterbot.corpus.english.conversations" )
	subscription_key = "541d952115be406b8a0dc8953c390631"
	endpoint = "https://api.cognitive.microsofttranslator.com"
			
	location = "eastus"
			
	path = '/translate'
	constructed_url = endpoint + path
			
	params = {
			'api-version': '3.0',
			'from': 'en',
			'to': ['zu']
	}
	constructed_url = endpoint + path
			
	headers = {
			'Ocp-Apim-Subscription-Key': subscription_key,
			'Ocp-Apim-Subscription-Region': location,
			'Content-type': 'application/json',
			'X-ClientTraceId': str(uuid.uuid4())
	}
	# sp= "Are you stupid?"
	response2 = chatbot.get_response(sp)

	body = [{
			'text': str(response2),
	}]

	ody = [{
			'text': str(sp),
	}] 
	request = requests.post(constructed_url, params=params, headers=headers, json=body)
	response = request.json()
	request1 = requests.post(constructed_url, params=params, headers=headers, json=ody)
	response1 = request1.json()

	p = json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
	z = p[p.find('\"text\":'):p.find(",")].replace('\"text\":',"").replace("\"","")
	p1 = json.dumps(response1, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
	z1 = p1[p1.find('\"text\":'):p1.find(",")].replace('\"text\":',"").replace("\"","")

	tts = gTTS("you typed"+sp+"in zulu"+z1+"then chatbot said"+str(response2)+"in zulu"+z) #Provide the string to convert to speech
	# tts.save('static/app/output.wav') #save the string converted to speech as a .wav file
	tts.save(os.path.join(settings.BASE_DIR, 'output.wav') )
	sound_file = 'output.wav'

	# Audio(sound_file, autoplay=True) 

	cnx = mysql.connector.connect(user="shraddhar", password="5@shade@rR", host="testg.mysql.database.azure.com", port=3306, database="db1")
	mycursor = cnx.cursor()
	# mycursor.execute("INSERT INTO dialogue (inpE,cbrE,cbrZ,inpZ) VALUES (' "+str(sp)+" ',' "+str(response2)+" ',' "+str(z)+" ',' "+z1+" ' "+" )")
	mycursor.execute('INSERT INTO dialogue (inpE,cbrE,cbrZ,inpZ) VALUES ("%s", "%s", "%s", "%s")' % (str(sp), str(response2), str(z), str(z1)))
	cnx.commit()
	cnx.close()
	mycursor.close()

def cloud():
  cnx2 = mysql.connector.connect(user="shraddhar", password="5@shade@rR", host="testg.mysql.database.azure.com", port=3306, database="db1")
  mycursor2 = cnx2.cursor()

  mycursor2.execute("SELECT * FROM dialogue")

  rows = mycursor2.fetchall()

  k = []

  for row in rows:
     k.append(row[2])
     k.append(row[3])
  comment_words = " ".join(k)+" "
  wordcloud = WordCloud(width = 500, height = 500,
                  background_color ='white',
                  min_font_size = 10).generate(comment_words)

  #wordcloud.to_file('static/app/wordcl.png')
  wordcloud.to_file(os.path.join(settings.BASE_DIR, 'wordcl.png'))
