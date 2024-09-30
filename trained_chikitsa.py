import numpy as np
from tensorflow.keras.models import load_model
import random
import json
from nltk import WordNetLemmatizer
import nltk

# Load trained model and necessary files
model = load_model('model/chikitsa_model.h5')
lemmatizer = WordNetLemmatizer()

with open('dataset/intents.json') as file:
    intents = json.load(file)

words, classes, documents = preprocess_data(intents)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence, model):
    bow_vector = bow(sentence, words)
    res = model.predict(np.array([bow_vector]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    for intent in intents_json['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])

# Chat with the bot
while True:
    message = input("You: ")
    ints = predict_class(message, model)
    res = get_response(ints, intents)
    print(f"Bot: {res}")
