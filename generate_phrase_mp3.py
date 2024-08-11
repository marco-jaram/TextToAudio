from gtts import gTTS
import os
import wave
import struct
import subprocess

def create_silent_wav(filename, duration=5):
    # Create a silent WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(44100)  # 44.1kHz sampling rate
        for _ in range(int(44100 * duration)):
            value = struct.pack('<h', 0)
            wav_file.writeframesraw(value)

def combine_audio_files(speech_file, silent_file, output_file):
    # Combine the MP3 with the silent WAV using FFmpeg
    command = [
        'ffmpeg',
        '-i', speech_file,
        '-i', silent_file,
        '-filter_complex', '[0:a][1:a]concat=n=2:v=0:a=1',
        '-y',  # Overwrite output file if it exists
        output_file
    ]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_mp3_files_with_end_silence(phrases, output_dir='phrase_audio', silence_duration=5):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create a silent WAV file
    silent_wav = 'silent.wav'
    create_silent_wav(silent_wav, silence_duration)

    for i, phrase in enumerate(phrases):
        print(f"Generating MP3 for: {phrase}")
        
        # Generate a temporary filename for the speech
        temp_speech_file = f"temp_speech_{i}.mp3"
        
        # Create a gTTS object and save the speech
        tts = gTTS(text=phrase, lang='en')
        tts.save(temp_speech_file)
        
        # Generate the final filename
        filename = f"{i+1:03d}_{phrase[:30].replace(' ', '_')}.mp3"
        filepath = os.path.join(output_dir, filename)
        
        # Combine the speech MP3 with the silent WAV
        combine_audio_files(temp_speech_file, silent_wav, filepath)
        
        # Remove temporary speech file
        os.remove(temp_speech_file)
        
        print(f"Saved: {filepath}")

    # Remove the silent WAV file
    os.remove(silent_wav)

def read_phrases_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

# File name of your phrases
phrases_file = 'english_phrases.txt'

# Read phrases from the file
english_phrases = read_phrases_from_file(phrases_file)

# Generate MP3 files for all phrases with a 5-second silence at the end
generate_mp3_files_with_end_silence(english_phrases)

print("All MP3 files have been generated with 5 seconds of silence at the end!")