from openai import openAI

client = openAI()

def create_assistant(name, instructions, tools):
    assistant = client.beta.assistants.create(
    name=name,
    instructions=instructions,
    tools=tools,
    model="gpt-4-turbo-preview")
    return assistant

def making_request(assistance, promt):
    thread = client.beta.threads.create()
    

