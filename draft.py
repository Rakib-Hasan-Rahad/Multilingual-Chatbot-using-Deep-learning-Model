import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

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
print("Let's chat! (type 'quit' to exit)")
current_context = None  # Initialize context variable

while True:
    sentence = input("You: ")
    if sentence == "quit":
        break

    # Check for context and update it
    if current_context:
        sentence = f"{current_context} {sentence}"
        current_context = None  # Reset context after using it

    sentence = tokenize(sentence)

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
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])

                # Check if the intent has a context set
                if "context_set" in intent:
                    current_context = intent["context_set"]

                print(f"{bot_name}: {response}")
    else:
        print(f"{bot_name}: I do not understand...")
