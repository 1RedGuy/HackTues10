import openai

def create_assistant(name, instructions, tools):
    assistant = client.beta.assistants.create(
    name=name,
    instructions=instructions,
    tools=tools,
    model="gpt-4-turbo-preview")
