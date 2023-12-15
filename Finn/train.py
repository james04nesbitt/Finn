import sqlite3
import json
import random
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, GlobalMaxPooling1D
from keras.optimizers import SGD
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

conn = sqlite3.connect('finn.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM TagData')


intents = {}
queries = []
responses = []
tags = []



for row in cursor.fetchall():
    tag = row[0]
    tag_queries = json.loads(row[1])  # Deserialize JSON strings to Python lists
    tag_responses = json.loads(row[2])
    
    # Add data to respective lists and intents dictionary
    intents[tag] = {'queries': tag_queries, 'responses': tag_responses}
    queries.extend(tag_queries)
    responses.extend(tag_responses)
    tags.extend([tag] * len(tag_queries))


tokenizer = Tokenizer()
tokenizer.fit_on_texts(queries)
sequences = tokenizer.texts_to_sequences(queries)
max_seq_length = max(len(seq) for seq in sequences)
padded_sequences = pad_sequences(sequences, maxlen=max_seq_length, padding='post')

def save_file(max_length):
    with open('maxseq.pkl', 'wb') as file:
        pickle.dump(max_length, file)

def load_file(): 
    with open('maxseq.pkl', 'rb') as file:
        max_length = pickle.load(file)
        return max_length


# Convert tags to categorical labels
tag_labels = np.array(tags)
unique_tags = np.unique(tag_labels)
label_indices = {label: index for index, label in enumerate(unique_tags)}
categorical_labels = np.array([label_indices[tag] for tag in tag_labels])

# Define neural network architecture
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=100, input_length=max_seq_length))
model.add(LSTM(128, return_sequences=True))
model.add(GlobalMaxPooling1D())
model.add(Dense(len(unique_tags), activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Split data into training and validation sets
train_sequences, val_sequences, train_labels, val_labels = train_test_split(padded_sequences, categorical_labels, test_size=0.2, random_state=42)

# Train the model
model.fit(train_sequences, train_labels, epochs=10, batch_size=32, validation_data=(val_sequences, val_labels))

model.save('finn.h5')