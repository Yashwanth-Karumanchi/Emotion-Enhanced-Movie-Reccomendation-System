from flask import Flask , render_template,request,jsonify
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.preprocessing.text import  Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
df_movies=pd.read_csv("H:/Abhi/pro/imdb_top_1000.csv")
ids=np.arange(1000).tolist()
df_movies['id']=ids


def get_tweets(data):
  tweets=data.text.values.tolist()
  labels=data.label.values.tolist()
  return tweets,labels
train=pd.read_csv('H:/Abhi/pro/train.csv')
tweets,labels = get_tweets(train)
tokenizer=Tokenizer(num_words=1000,oov_token='<UNK>')
tokenizer.fit_on_texts(tweets)
tokenizer.texts_to_sequences([tweets[0]])
maxlen=50
def get_sequences(tokenizer,tweets):
  sequences=tokenizer.texts_to_sequences(tweets)
  padded=pad_sequences(sequences,truncating='post',padding='post',maxlen=maxlen)
  return padded

model_instance=tf.keras.models.load_model("H:/Abhi/pro/model_instance_20epochs")



app=Flask(__name__)
@app.route('/',methods=['GET'])

def dummy():
    response=jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict',methods=['POST'])
def predict():
    inp=request.form['text']
    print(inp)
    response=jsonify({
        'prediction':predict(inp)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def predict(inp):
    mood_input=inp
    string=get_sequences(tokenizer,[mood_input])
    p=model_instance.predict(string)[0]
    print(p)
    res=np.argmax(p).astype('uint8')
    print(res)
    temp=["Drama","Horror","Romance","Biography","Romance","Animation"]
    given_genre=temp[res]
    print(given_genre)
    vectorizer = TfidfVectorizer()
    vectorizer.fit(df_movies['Genre'])
    tfidf = vectorizer.transform([given_genre])
    similarity = cosine_similarity(tfidf, vectorizer.transform(df_movies['Genre']))
    movie_ids = list(df_movies.loc[similarity.argsort()[0][-10:]]['id'])
    movie_names=df_movies.loc[df_movies['id'].isin(movie_ids),'Series_Title'].tolist()
    movie_names.reverse()
    posters=df_movies.loc[df_movies['id'].isin(movie_ids),'Poster_Link'].tolist()
    posters.reverse()
    dic=dict(zip(movie_names,posters))
    return dic
    
if __name__ == "__main__":
    
    app.run(port=3000,debug=True)


