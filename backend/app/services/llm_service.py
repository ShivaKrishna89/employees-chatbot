from openai import OpenAI
import os


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def loadPrompt():
    with open('prompts/nlu_prompts.txt','r') as prompt:
        return prompt.read().strip()

def loadAttachmentPrompt():
    with open('prompts/attachment_prompt.txt','r') as prompt:
        return prompt.read().strip()



def get_api_response_for_prompt(user_input: str):
    SYSTEM_PROMPT = loadPrompt()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=1,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

def get_api_response_for_attachment(content: str, userInput:str):
    SYSTEM_PROMPT = loadPrompt()
    combined_prompt = f"User input (intent):{userInput} Resume content:{content}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=1,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": combined_prompt}
        ]
    )
    return response.choices[0].message.content
