from openai import OpenAI
import openai, os
import time, logging
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

class Model_Service():
    def __init__(self, name, instructions, tools):
        self.client = OpenAI()
        self.model_assistance = self.client.beta.assistants.create(
        name=name,
        instructions=instructions,
        tools=tools,
        model="gpt-3.5-turbo-16k"
    )
        self.assistant_id = self.model_assistance.id

    def run_model(self):
        print(self.thread_id, self.assistant_id)
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id
        )
        self.run_id = run.id

    def input_message(self, message, upload_file: bool = False, file_id = None):
        file_ids = []
        if upload_file is True and file_id is not None:
            file_ids.append(file_id)
        elif upload_file is True and file_id is None:
            raise ValueError("You must provide a file_id if upload_file is True")
        
        thread = self.client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": str(message),
                "file_ids": file_ids
            }
        ]
        )
        self.thread_id = thread.id
        self.run_model()

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
                    print(f"Assistant Response: {response}")
                    break 
            except Exception as e:
                logging.error(f"An error occurred while retrieving the run: {e}")
            logging.info("Waiting for run to complete...")
            time.sleep(sleep_interval)
