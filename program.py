import nltk
import numpy as np
nltk.download('punkt')
nltk.download('wordnet')
import string
import warnings
warnings.filterwarnings("ignore")
 
 
memory='hello. '
sent=nltk.sent_tokenize(memory)
 
 
lemmer = nltk.stem.WordNetLemmatizer()      #object
 
 
#Lemmatizing
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
 
 
 
 
#creating dict of punctuations
remove_punct_dict = dict((ord(punct),None) for punct in string.punctuation)
 
 
 
 
#removing puctuations , lower
def Normalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
 
 
 
 
#TF - IDF
from sklearn.feature_extraction.text import TfidfVectorizer
#Importing
from sklearn.metrics.pairwise import cosine_similarity
 
 
 
 
 
#defining bot response
def response(user_response):
    user_response=user_response.lower()
 
    if user_response == "/start" or user_response=="hey":
        robo_response='''
Hi, My name is Dobby .
Tell me anything and I will remember it for you.
 
(Eg- Just say : Hey dobby , remember that ______________.)
        '''
        return robo_response
 
    elif ("remember that" in user_response):
        robo_response ="""
Alright I have stored it in my Brain.
You can ask me anytime.
        """
        words=user_response.split()
        words=words[words.index("that")+1:]
        words=" ".join(words)
        sent.append(words)
        return robo_response
 
    else:
        robo_response = " "
        sent.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer= Normalize,stop_words="english" )
        tfidf = TfidfVec.fit_transform(sent)
        vals = cosine_similarity(tfidf[-1],tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_fidf = flat[-2]
        if req_fidf== 0 :
            
            robo_response="Sorry ,You havn't told me this before. Please try again."
            sent.remove(sent[-1])
            return robo_response
        else:
            
            robo_response = "I remember you told me that ' "+sent[idx]+"'"
            sent.remove(sent[-1])
            return robo_response
    
 
 
import requests
import json
 
 
class telegram_bot():
    def __init__(self):
        self.token = "1152737745:AAGo_kZTRw7TS5W8tBckY99qb29tH2IhlAo"
    
        self.url = f"https://api.telegram.org/bot{self.token}"
 
    def get_updates(self,offset=None):
        url = self.url+"/getUpdates?timeout=100"
        if offset:
            url = url+f"&offset={offset+1}"
        url_info = requests.get(url)
        return json.loads(url_info.content)
 
    def send_message(self,msg,chat_id):
        url = self.url + f"/sendMessage?chat_id={chat_id}&text={msg}"
        if msg is not None:
            requests.get(url)
 
    def grab_token(self):
        return tokens
tbot = telegram_bot()
 
update_id = None
 
def make_reply(msg):
    if msg is not None:
 
        reply = response(user_response=msg)
    return reply
 
 
 
 
while True:
    print("...")
    print(sent)
    updates = tbot.get_updates(offset=update_id)
    updates = updates['result']
    print(updates)
    if updates:
        for item in updates:
            update_id = item["update_id"]
            print(update_id)
            try:
                message = item["message"]["text"]
                print(message)
            except:
                message = None
            from_ = item["message"]["from"]["id"]
            print(from_)
 
            reply = make_reply(message)
            tbot.send_message(reply,from_)
