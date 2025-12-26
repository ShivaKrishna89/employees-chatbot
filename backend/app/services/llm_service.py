from openai import OpenAI
import os


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def loadPrompt():
    with open('prompts/nlu_prompts.txt','r') as prompt:
        return prompt.read().strip()


SYSTEM_PROMPT = loadPrompt()

def get_api_response(user_input: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=1,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content
