import json
from sqlalchemy.orm import Session
from fastapi import APIRouter
from services.llm_service import get_api_response
from crud.employee import getEmployee,CreateEmployee
from db.db import session
from fastapi import Depends
chat = APIRouter()


def get_db():
  db = session()
  try:
    yield db
  finally:
    db.close()

@chat.get('/chat')
def getChat(userInput:str,db: Session = Depends(get_db)
):
    resp = get_api_response(userInput)
    resp = json.loads(resp)
    print(resp)
    intent = resp["intent"]
    name = resp["name"]
    department = resp["department"]
    return proceed(intent,name,department,db)


def proceed(intent,name,department, db: Session):
    resp = None
    match(intent):
        case 'CHECK':
            resp = getEmployee(name,department, db)
        case 'CREATE':
            if department is None:
               resp = "Please mention department to create employee"
            else:
               resp = CreateEmployee(name,department, db)
    return resp
