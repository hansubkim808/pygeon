import openl3
import soundfile as sf
import librosa 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import librosa.display
import tensorflow as tf
from tensorflow.keras import datasets, layers, models, Model
from keras.models import Sequential
from keras.layers.core import Lambda, Flatten, Dense
from keras.layers.pooling import MaxPooling2D
from keras.layers import Conv2D, Activation, Input
from tensorflow.keras.optimizers import Adam
from keras import backend as K
from PIL import Image
import glob
import cv2

def embCNN_model():
    # Resized embedding is a 32x32 Numpy array, which can be fed into the CNN as a grayscale image
    left_input = Input((32, 32, 1))
    right_input = Input((32, 32, 1))
    emb_model = models.Sequential() 
    emb_model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 1)))
    emb_model.add(layers.MaxPooling2D(2, 2))
    emb_model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    emb_model.add(layers.MaxPooling2D(2, 2))
    emb_model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    emb_model.add(layers.MaxPooling2D(2, 2))
    emb_model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    emb_model.add(Flatten())
    emb_model.add(Dense(2048, activation='sigmoid'))
    emb_model.summary() 

    # Feature vectors for pairwise deep audio embeddings 
    left_emb = emb_model(left_input)
    right_emb = emb_model(right_input)

    # Compute distance (L2) between 2 embedding feature vectors 
    l2_layer = Lambda(lambda x:K.sqrt(K.sum(K.square(x[0] - x[1]))))
    l2_distance = l2_layer([left_emb, right_emb])

    # Return similarity score between the 2 input song embeddings (left_input & right_input) 
    prediction = Dense(1, activation='softmax')(l2_distance)

    # Initialize Siamese Net
    siamese_net = Model(inputs=[left_input, right_input], outputs=prediction)

    siamese_net.compile(loss='binary_crossentropy', metrics=['acc'], optimizer=Adam(0.0001))

    siamese_net.summary() 

    return siamese_net


def melCNN_model():
    # Mel spectrogram (Resized image) is a 128x128 px image, with dim=3 for RGB 
    left_input = Input((128, 128, 3))
    right_input = Input((128, 128, 3))


    mel_model = models.Sequential() 
    # Default Keras values. These will be tweaked in the future depending on performance 
    mel_model.add(layers.Conv2D(64, (10, 10), activation='relu', input_shape=(128, 128, 3)))
    mel_model.add(MaxPooling2D())
    mel_model.add(layers.Conv2D(128, (7, 7), activation='relu'))
    mel_model.add(MaxPooling2D())
    mel_model.add(layers.Conv2D(128, (4, 4), activation='relu'))
    mel_model.add(MaxPooling2D())
    mel_model.add(layers.Conv2D(256, (4, 4), activation='relu'))
    mel_model.add(Flatten())
    mel_model.add(Dense(4096, activation='sigmoid'))

    left_mel = mel_model(left_input)
    right_mel = mel_model(right_input)

    # L2 Distance layer for similarity score 
    l2_layer = Lambda(lambda x:K.sqrt(K.sum(K.square(x[0] - x[1]))))
    l2_distance = l2_layer([left_mel, right_mel])

    # Softmax activation for classification 
    prediction = Dense(1, activation='softmax')(l2_distance)

    # Initialize Siamese Net 
    siamese_net = Model(inputs=[left_input, right_input], outputs=prediction)

    siamese_net.compile(loss='binary_crossentropy', metrics=['acc'], optimizer=Adam(0.0001))

    siamese_net.summary() 

    return siamese_net







