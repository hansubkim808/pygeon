import openl3
import soundfile as sf
import librosa 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import librosa.display
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from PIL import Image
import glob
import cv2

# The main motivation behind this script is to provide a clearer direction for producer 
# collaboration, artist collaboration, networking, and promotion for UNDERGROUND RAP ARTISTS. 
#
# Most "genre-classification" or existing song recommendation engines are quite general and thus 
# less accurate than would prove to be actually useful for music marketing/promotion. 
#  
# Through platforms such as Instagram, TikTok, and Triller, Rap music is BY FAR the fastest 
# growing genre being skyrocketed by the accessibility of social media. Yet, there is no dedicated 
# rap music classification system or recommendation engine by which smart pipelines can be 
# constructed for collaboration among artists of similar subgenres, flows, cadences, production 
# preferences, etc. 
# 
# This script is the beginning of what will hopefully become a comprehensive rap marketing toolkit 
# utilizing raw musical data (deep embeddings of songs and music videos) as well as social media 
# presence (relational data from Instagram) to optimize engagement and successful music output. 


# Rap Subgenres (As specified in this script): 

# 1) Modern Southern 1
#       Louisiana Sound, characterized by flanged guitars, aggressive mid-tempo trap hi-hats.
#       Primarily acoustic instrumentation (piano, guitar, organs, strings, bass guitar or 
#       funk bass in place of traditional 808). 
#
#       REPRESENTATIVE ARTISTS: NBA Youngboy, Fredo Bang, JaydaYoungan. 
# 
# 2) Florida 1
#       Florida rap sound - characterized by sparse, dark melody (usually a combination of 
#       low-register piano or strings, occasionally choir), with minimal/4 beat hi-hat drums.
#       Bass is primarily Spinz 808, with occasional extra sub-bass/Reese. 
#
#       REPR. ARTISTS: JDot Breezy, SpotemGottem, Nardo Wick, Spinabenz 
#
# 3) Introspective 1
#       Mellow, pop-esque melodic backing characterized by catchy, melancholy guitar loop.
#       Vocal one shots and soul/blues a cappella background vocals are common. Usually 
#       sparse but regular drumwork; lighter 808 (close to Pierre).  
#
#       REPR. ARTISTS: Hotboii, NoCap, Hurricane Wisdom, Rylo Rodriguez
#
# 4) Introspective 2
#       Sad, dark piano melodies, similar in fashion to Introspective 1, accompanied by 
#       Souls/blues vocal one-shots, reese bass, strings, soaring guitars, and hard-hitting 
#       kicks accompanied by sub-bass 808s. 
#
#       REPR. ARTISTS: Rod Wave, Polo G, Lil Durk 
# 
# 5) West Coast 1
#       Sparse, minimal trap beats in double time, characterized by a simple, haunting 
#       4-5 note piano melody and double-time drums. The quintessentiaL low-effort LA beat. 
#       Surprisingly incredibly popular. 
#
#       REPR. ARTISTS: 1TakeJay, 1TakeQuan, AzChike
# 
# 6) West Coast 2
#       More upbeat, bouncy double-time west coast trap beats, with occasional soul samples
#       and/or backing vocals. Upbeat chord progressions with slightly faster tempo than 
#       West Coast 1. Bouncy synth bass ("DJ Mustard bass") or soft muted kicks with light 808. 
# 
#       REPR. ARTISTS: 1TakeOcho, Baby Stone Gorillas
#
# 7) West Coast 3 (Soft)
#       REPR. ARTISTS: Bino Rideaux, Blxst, KalanFrFr
#
# 8) West Coast 4 (G-Funk Era)
#       REPR. ARTISTS: G Perico, Rucci, Stupid Young 
#
# 9) West Coast 5 (Dark) 
#       REPR. ARTISTS: Drakeo the Ruler, Ralfy, SaySo, Remble 
# 
# 10) West Coast 6 (Bay Area/Modern Hyphy)
#       REPR. ARTISTS: Shootergang Kony, DaBoii, ALLBLACK, Mike Sherm
#
# 11) Modern Popular 1 (Hard Trap) 
#       REPR. ARTISTS: Pooh Shiesty, King Von, NLE Choppa
#
# 12) Modern Popular 2 (Minimal Trap)
#       REPR. ARTISTS: BigKayBeezy, 
# 
# 13) Modern Popular 3 (YSL Guitar) 
#       REPR. ARTISTS: Gunna, Lil Keed, Young Thug 
# 
# 14) Modern Southern 2 (Relaxed Louisiana)
#       REPR. ARTISTS: Da Real Gee Money, Fredo Bang 
# 
# 15) Introspective 3 (Blues Revival, Modern Pain Combo) 
#       REPR. ARTISTS: Rod Wave, Lil Poppa, Yungeen Ace
# 
# 16) Modern Popular 4 (Rage Beats/Off Kilter Flow) 
#       REPR. ARTISTS: SSGKobe, KSuave, SoFaygo 
# 
# 17) Florida 2 (Irreverent, Off Kilter)
#       REPR. ARTISTS: 9lokknine, Trapland Pat, Soldier Kidd
# 
# 18) New York Drill
#       REPR. ARTISTS: Pop Smoke, Kay Flock, Sheff G, 22Gz

# Create, crop, and process Mel Spectrogram images for entire rap song dataset 

# Create a vector of softmax values revealing incorporation/influence of each of the subgenres listed above 

# Stores raw wav files of songs (training data)
t_wav_dir = "../training/raw_wavs/"

# Stores raw ground truth values (category)
t_label_dir = "../training/wav_labels/"

# Stores all deep embeddings of wavs
t_embed_dir = "../training/embeddings/"

# Stores all mel spectrograms of wavs
t_melspec_dir = "../training/mel_spectrograms/"

# Stores all resized mel spectrograms of wavs 
t_mini_dir = "../training/mel_spec_resized/"

# Stores all resized deep embeddings of wavs 
t_deep_mini_dir = "../training/embed_resized/"

all_wavs = glob.glob(t_wav_dir + "*.wav");
all_labels = glob.glob(t_label_dir + "*.txt")

default_model = openl3.models.load_audio_embedding_model(input_repr='mel256', 
                                                         content_type='music',
                                                         embedding_size=512)

for wav in all_wavs:
    # Parse unique song identifier 
    song_id = wav[len(t_wav_dir):len(t_wav_dir)+len(wav)-5]


    # Create Openl3 embeddings of all wavs in training data
    aud, sr = sf.read(wav)
    emb, ts = openl3.get_audio_embedding(aud, sr, model=default_model)
    # Each embedding is saved as a 2D numpy array (computational equivalent of a grayscale image)
    openl3.process_audio_file(t_wav_dir, suffix=song_id, output_dir=t_embed_dir)
    # Future additions: use multiple consecutive clips in one wav file, each of different length;
    # compute 2D embedding for each of them and stack them on top of each other for 3D array 


    # Create Librosa Mel Spectrogram of all wavs in training data 
    y, srt = librosa.load(wav)
    spect = librosa.feature.melspectrogram(y=y, sr=srt, n_fft=2048, hop_length=512)
    spect = librosa.power_to_db(spect, ref=np.max)
    fig = plt.figure()
    mel_spec_file_dir = t_melspec_dir + "mel_spec_" + song_id + ".png"
    fig.savefig(mel_spec_file_dir)

all_melspecs = glob.glob(t_melspec_dir + "mel_spec_*.png")
all_embeds = glob.glob(t_embed_dir + "*.npz")

# Resize all full mel spectrograms to fit the CNN 
for fs_image in all_melspecs: 
    reg_size = Image.open(fs_image)
    mini_png = reg_size.resize((128, 128))
    mini_png.save(t_mini_dir + "mel_spec_" + song_id + "_mini.png")

# Resize all full deep embeddings to fit the CNN 
# (Background Context: ) Deep embeddings are huge, much larger 
# than regular images (4 figures of pixels for both height and width). 
# We want to compress these, while maximizing information expressivity 
for fs_embedding in all_embeds:
    data = np.load(fs_embedding)
    emb = data['embedding']
    # Compressing/resizing image with Inter-Area interpolation; 
    # other "pixel" interpolation methods exist but haven't tried yet 
    mini_emb = cv2.resize(emb, dsize=(32, 32), interpolation=cv2.INTER_AREA)
    mini_emb_dir = t_deep_mini_dir + song_id + "_mini_embedding.png"

    # At this point, mini embeddings are saved as ".png", and full-size 
    # embeddings are saved as ".npz" because OpenCV does not have a native 
    # embedding file extension compatible with OpenL3
    cv2.imwrite(mini_emb_dir, mini_emb)










