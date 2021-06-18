import streamlit as st
import os
from pydub import AudioSegment
import wave
from google.cloud import storage


is_check = st.checkbox("Unlock Audio file conversion")

if is_check:
    audio_file_name = st.file_uploader(
        "Upload Your Audio File", type=['mp3', 'wav'])
    if audio_file_name is not None:
        file_details = {"FileName": audio_file_name.name,
                        "FileType": audio_file_name.type, "FileSize": audio_file_name.size}
        # st.write(file_details)

# Converting mp3 to wav format


def mp3_to_wav(audio_file_name):
    if audio_file_name.split('.')[1] == 'mp3':
        sound = AudioSegment.from_mp3(audio_file_name)
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(audio_file_name, format="wav")

# Converting Frame_rate


def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        print("\n\n** FILE CONVERSION SUCCESSFUL **")
        channels = wave_file.getnchannels()
        return frame_rate, channels

# Converting stereo to mono, i.e. changing to 1 channel


def stereo_to_mono(audio_file_name):
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")


# Uploading audio file to Google Cloud
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

# Deleting audio file


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()
