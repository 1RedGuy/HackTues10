from openai import OpenAI
import openai, os
import time, logging
from datetime import datetime
from dotenv import load_dotenv
from mutagen.mp3 import MP3
from mp3_utils import MP3_Service

load_dotenv()

class Model_Service():
    def __init__(self, mp3_file_pathm, txt_target_path):   
        self.client = OpenAI()
        self.mp3_file_pathm = mp3_file_pathm
        self.txt_target_path = txt_target_path

    def run_file(self):
        self.file = self.client.files.create(
            file = open(self.conversation, 'rb'),
            purpose = "assistants"
        )
        return self.file.id

    def run_model(self, assistant_id):
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=assistant_id
        )
        self.run_id = run.id

    def input_message(self, message, assistant_id):
        thread = self.client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": str(message),
                    "file_ids": [self.run_file()]
                }
            ]
          )
        self.thread_id = thread.id
        self.run_model(assistant_id)
        return thread.id

    def wait_for_run_completion(self, client, sleep_interval):
        thread_id = self.thread_id
        run_id = self.run_id
        while True:
            try:
                run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
                if run.completed_at:
                    elapsed_time = run.completed_at - run.created_at
                    formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                    print(f"Run completed in {formatted_elapsed_time}")
                    logging.info(f"Run completed in {formatted_elapsed_time}")

                    messages = client.beta.threads.messages.list(thread_id=thread_id)
                    last_message = messages.data[0]
                    response = last_message.content[0].text.value
                    return response
            except Exception as e:
                logging.error(f"An error occurred while retrieving the run: {e}")
            logging.info("Waiting for run to complete...")
            time.sleep(sleep_interval)
    
    def mp3_to_json(self, message_to_assistant):
        stt_class = MP3_Service(self.mp3_file_pathm, self.txt_target_path)


        self.conversation = stt_class.coversation_target_path
        text_to_text = self.client.beta.assistants.create(
            name= "EduNova Assistant",
            instructions= os.getenv("ASSISTANT_INSTRUCTIONS"),
            tools= [{"type": "retrieval"}],
            model= "gpt-4-turbo-preview",
            file_ids= None
        )

        self.input_message(message_to_assistant, text_to_text.id)
        self.response = self.wait_for_run_completion(self.client, 5)
        return self.response



