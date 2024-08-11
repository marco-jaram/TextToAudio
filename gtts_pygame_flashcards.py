from gtts import gTTS
import pygame
import os
import time

def text_to_speech(phrases, lang='en'):
    pygame.mixer.init()
    for i, phrase in enumerate(phrases):
        print(f"Playing: {phrase}")
        
        # Create a gTTS object
        tts = gTTS(text=phrase, lang=lang)
        
        # Save the audio file
        filename = f"phrase_{i}.mp3"
        tts.save(filename)
        
        # Play the audio file
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # Remove the audio file after playing
        pygame.mixer.music.unload()
        os.remove(filename)
        
        time.sleep(1)  # Pause for a second between phrases

def read_phrases_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

# File name of your phrases
phrases_file = 'english_phrases.txt'

# Read phrases from the file
english_phrases = read_phrases_from_file(phrases_file)

# Call the function with your phrases
text_to_speech(english_phrases)