from openai import OpenAI
from utils import create_assistant
from os import getenv

client = OpenAI()

prompt = os.getenv("PROMPT")

create_assistant("EduNova Assitant", prompt, instructions="")
  
