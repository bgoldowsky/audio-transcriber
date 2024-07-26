# Notes:
# Set up Google Cloud project and access to that project for users of this script.
# Activate the Google Cloud Speech-to-Text API for the project.
#
# One-time setup on developer machine:
# Install gcloud command line tools; steps in https://cloud.google.com/sdk/docs/install
# brew install python
# brew install ffmpeg
# Create directory for this work and cd into it.
# /opt/homebrew/bin/python3 -m venv venv
# source venv/bin/activate
# pip install --upgrade google-cloud-speech pydub
#
# To run (we'll make this simpler eventually):
# cd to the audio-transcriber directory
# source venv/bin/activate
# cd src
# python main.py

# TODO: detect speakers. https://cloud.google.com/speech-to-text/docs/multiple-voices

from pydub import AudioSegment
from google.cloud import speech

audio_file_path = "../audio/test-audio.m4a"

def transcribe(path) -> speech.RecognizeResponse:
    client = speech.SpeechClient()

    flac_file_path = "./test-audio.flac"
    
    audio = AudioSegment.from_file(path)
    # Just use the part starting at 2:00, which includes multiple speakers.
    audio_sample = audio[120000:]

    # Convert to FLAC format
    audio_sample.export(flac_file_path, format="flac")

    # Read audio bytes from a local file
    with open(flac_file_path, "rb") as audio_file:
       audio = speech.RecognitionAudio(content=audio_file.read())

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)
    # print(response)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

transcribe(audio_file_path)
