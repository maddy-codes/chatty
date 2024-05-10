from openai import OpenAI
import os

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")




def make_questions(data):
    completion = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=[
            {
                "role": "system",
                "content": "You are a university of Northampton AI Course bot, made to anwer student queries around the course and uni! Please can you rephrase the [answer] according to the [question]! Please be formal and cordial! Do not add irrelevant explaination",
            },
            {
                "role": "user",
                "content": "[answer] = classes this week Computer science (2 april), AI PRogramming (3 April) Relational Database (6th April) [question] = When is my next class?",
            },
        ],
        temperature=0.1,
    )
    return completion.choices[0].message.content


    