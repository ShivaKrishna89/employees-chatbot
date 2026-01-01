import json
import os
from sqlalchemy.orm import Session
from fastapi import APIRouter, File, HTTPException, UploadFile, Form
from services.llm_service import get_api_response_for_prompt,get_api_response_for_attachment
from crud.employee import getEmployee,createEmployee, updateEmployee, deleteEmployee
from db.db import session
from fastapi import Depends
chat = APIRouter()
from pypdf import PdfReader
import io

def get_db():
  db = session()
  try:
    yield db
  finally:
    db.close()

@chat.get('/chat')
def getChat(userInput:str,db: Session = Depends(get_db)
):
    resp = get_api_response_for_prompt(userInput)
    resp = json.loads(resp)
    print(resp)
    intent = resp["intent"]
    name = resp["name"]
    department = resp["department"]
    updateField = resp.get('updateField')
    newValue = resp.get('newValue')
    return proceed(intent,name,department,updateField,newValue,db)


def proceed(intent,name,department,updateField,newValue, db: Session):
    resp = None
    match(intent):
        case 'CHECK':
            resp = getEmployee(name,department, db)
        case 'CREATE':
            if department is None:
               resp = "Please mention department to create employee"
            else:
               resp = createEmployee(name,department, db)
        case 'UPDATE':
            if department is None:
               resp = "Please mention department to update employee"
            else:
               resp = updateEmployee(name,department,updateField,newValue, db)
        case 'DELETE':
            if department is None:
               resp = "Please mention department to delete employee"
            else:
               resp = deleteEmployee(name,department, db)
    return resp

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


@chat.post('/upload')
async def upload_file(file: UploadFile = File(...),userInput: str = Form(""),db: Session = Depends(get_db)):
    try:
      file_bytes = await file.read()
      file.file.seek(0)
      if file.content_type != "application/pdf":
          raise HTTPException(status_code=400, detail="Only PDFs supported")

      content = extract_text_from_pdf(file_bytes)

      resp = get_api_response_for_attachment(content, userInput)
      resp = json.loads(resp)
      print(resp)
      intent = resp["intent"]
      name = resp["name"]
      department = resp["department"]
      updateField = resp.get('updateField')
      newValue = resp.get('newValue')
      return proceed(intent,name,department,updateField,newValue,db)
    except Exception as e:
       resp = {"intent": None, "name": None, "department": None}
    finally:
        await file.close()



