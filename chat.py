import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from langdetect import detect
from translate import Translator

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Kesleiv"
current_context = None  # Initialize current_context variable

# Function to detect the language of a text
def detect_language(text):
    try:
        language = detect(text)
        return language
    except:
        return "Unknown"

# Function to translate text to English
def translate_to_english(text):
    translator = Translator(provider='mymemory', from_lang='bn', to_lang='en')
    translation = translator.translate(text)
    return translation

# Function to translate text to Bangla
def translate_to_bangla(text):
    translator = Translator(provider='mymemory', from_lang='en', to_lang='bn')
    translation = translator.translate(text)
    return translation

def get_response(msg):
    global current_context  # Use the global variable

    # Detect the language of the user input
    detected_language = detect_language(msg)

    # Check if the detected language is Bangla
    if detected_language == 'bn':
        # Translate user input to English
        msg = translate_to_english(msg)

    # Check for context and update it
    if current_context and not any(context in msg for context in current_context):
        msg = f"{current_context[0]} {msg}"

    sentence = tokenize(msg)

    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    # Check if the confidence is high and handle context
    if prob.item() > 0.75:
        response = None  # Initialize response variable

        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])

                # Check if the intent has a context set
                if "context_set" in intent:
                    current_context = intent["context_set"]
                    break  # Break the loop after finding a matching intent

        # Check if the detected language is Bangla and translate the response
        if detected_language == 'bn':
            response = translate_to_bangla(response)

        return response

    return "I do not understand..."
