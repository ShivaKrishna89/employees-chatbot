from fastapi import APIRouter
from services.llm_service import get_api_response
chat = APIRouter()




@chat.get('/chat')
def getChat(userInput:str):
    resp = get_api_response(userInput)
    return resp
