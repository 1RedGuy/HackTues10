from openai import OpenAI
from utils import create_assistant, making_request
import os

prompt = os.getenv("PROMPT")

create_assistant("EduNova Assitant", prompt, instructions="This is a test", tools="all")
making_request("EduNova Assitant", "This is a test")

