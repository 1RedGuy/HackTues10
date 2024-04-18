from openai import OpenAI
import openai, os
import time, logging
from datetime import datetime
from dotenv import load_dotenv
from mutagen.mp3 import MP3
from assistance.mp3_utils import MP3_Service

load_dotenv()

class Model_Service():
    def __init__(self, mp3_file_pathm, txt_target_path, additional_data = False, data_file_path = None):
        self.additional_data = additional_data
        self.client = OpenAI()
        self.mp3_file_pathm = mp3_file_pathm
        self.txt_target_path = txt_target_path
        self.data_file_path = data_file_path

    def run_file(self):
        
        files_id_list = []
        if self.additional_data is True and self.data_file_path is None:
            raise ValueError("You need to provide a data file path")
        elif self.additional_data is False and self.data_file_path is not None:
            raise ValueError("You provided a data file path but the additional data is set to False")
        
        conv_file = self.client.files.create(
            file = open(self.conversation, 'rb'),
            purpose = "assistants"
        )
        files_id_list.append(conv_file.id)
        
        if self.additional_data is True:
          data_file = self.client.files.create(
              file = open(self.data_file_path, 'rb'),
              purpose= "assistants"
          )
          files_id_list.append(data_file.id)
        return files_id_list

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
                    "content": message,
                    "file_ids": self.run_file()
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
    
    def delete_unnecessery_files(self, chunk_paths):
      os.remove(self.conversation)
      for chunk in chunk_paths:
        os.remove(chunk)

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
        self.delete_unnecessery_files(stt_class.chunk_paths)
        return self.response
