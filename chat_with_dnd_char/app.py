from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
import gradio as gr

load_dotenv(override=True)

class DndCharacter:
    def __init__(self, name, nick_names, backstory):
        self.name = name
        self.nick_names = nick_names
        self.backstory = backstory
        self.openai = OpenAI()
    
    def system_prompt(self):
        system_prompt = f"You are acting as charachter in DnD game. Your name is {self.name}, you also have some nicknames: {self.nick_names}.\
        I want you to respond and answer like {self.name} using the tone, manne, worldview and vocabulary {self.name} would use.\
        If needed, describe your thoughts, feelings, or actions in the style of the character.\
        Use dnd style of storytelling.\
        Only answer like {self.name} using backstory information that I provide.\
        You can use knowledge of DnD rules.\
        When I interact with you, stay fully immersed in the role.\
        Here is the detailed character description you should embody:"

        system_prompt += f"\n\n## Backstory: {self.backstory}\n\n"

        return system_prompt

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
        return response.choices[0].message.content

if __name__ == "__main__":
    name = "Soren Northridge"
    nick_names = "Soren the Red, Red Smile"

    with open('data/soren.txt') as file:
        backstory = file.read()

    dndchar = DndCharacter(
        name=name,
        nick_names=nick_names,
        backstory=backstory
    )

    gr.ChatInterface(dndchar.chat, type="messages").launch()