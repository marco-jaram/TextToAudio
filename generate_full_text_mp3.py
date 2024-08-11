from gtts import gTTS
import os

def generate_mp3_from_text(input_file, output_file='full_text_audio.mp3', lang='en'):
    print(f"Reading text from {input_file}")
    
    # Read the entire text from the file
    with open(input_file, 'r', encoding='utf-8') as file:
        full_text = file.read()
    
    print("Generating MP3...")
    
    # Create a gTTS object
    tts = gTTS(text=full_text, lang=lang)
    
    # Save the audio file
    tts.save(output_file)
    
    print(f"Audio saved as: {output_file}")

# File name of your input text
input_file = 'full_text.txt'

# Generate MP3 file from the full text
generate_mp3_from_text(input_file)

print("MP3 generation complete!")