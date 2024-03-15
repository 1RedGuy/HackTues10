from mutagen.mp3 import MP3
from openai import OpenAI
from pydub import AudioSegment
import os
from dotenv import load_dotenv
load_dotenv()

class MP3_Service():
    def __init__(self, file_path, target_path):
        self.file_path = file_path
        self.target_path = target_path
        self.chunk_size_mb=8
        audio = MP3(file_path)
        file_size_bytes = os.path.getsize(file_path)
        bitrate = audio.info.bitrate
        sec_duration = (file_size_bytes * 8) / bitrate
        chunk_size_bytes = self.chunk_size_mb * 1024**2
        bitrate_per_chunk = chunk_size_bytes * 8
        duration_per_chunk_sec = bitrate_per_chunk / bitrate
        self.total_chunks = sec_duration / duration_per_chunk_sec
        self.save_chunks()
        self.speech_to_text()

    def save_chunks(self):
        if not os.path.exists(self.target_path):
            os.makedirs(self.target_path)
        self.chunk_paths = []
        audio = AudioSegment.from_mp3(self.file_path)
        file_size_bytes = os.path.getsize(self.file_path)
        bitrate = audio.frame_rate * audio.frame_width * audio.channels * 8
        chunk_size_bytes = self.chunk_size_mb * 1024**2
        duration_per_chunk_ms = (chunk_size_bytes / file_size_bytes) * len(audio)
        self.total_chunks = int(len(audio) / duration_per_chunk_ms) + (len(audio) % duration_per_chunk_ms > 0)
        
        for i in range(self.total_chunks):
            start_ms = i * duration_per_chunk_ms
            end_ms = start_ms + duration_per_chunk_ms
            if end_ms > len(audio):
                end_ms = len(audio)
            chunk = audio[start_ms:end_ms]
            chunk_file_name = os.path.join(self.target_path, f"chunk{i+1}.mp3")
            self.chunk_paths.append(chunk_file_name)
            chunk.export(chunk_file_name, format="mp3")
            print(f"Exported {chunk_file_name}")

    def speech_to_text(self):
        client = OpenAI()
        self.coversation_target_path = os.path.join(os.getcwd(), "conversation.txt")
        for chunk in self.chunk_paths:
            audio_file = open(chunk, "rb")
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file, 
                response_format="text"
            )
            with open(self.coversation_target_path, "a") as file:
                print(transcription)
                file.write(transcription + "\n")
        return self.coversation_target_path
        
