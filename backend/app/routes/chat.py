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
from schema.schema import LLMResponseSchemaForInput

def get_db():
  db = session()
  try:
    yield db
  finally:
    db.close()

@chat.get('/chat/text')
def getChat(userInput:str,db: Session = Depends(get_db)
):
    llm_response = get_api_response_for_prompt(userInput)
    print(llm_response)
    try:
      jsonResp = json.loads(llm_response)
      parsed = LLMResponseSchemaForInput(**jsonResp)
      result = proceed(
          parsed.intent,
          parsed.name,
          parsed.department,
          parsed.updateField,
          parsed.newValue,
          db,
      )
      return {"response": result}
    except Exception:
        return {"response": "Invalid LLM response"}




def proceed(intent,name,department,updateField,newValue, db: Session):
    if not intent:
      return "Please ask something about an employee, like checking, creating, updating, or deleting."
    intent = intent.upper()
    if department is None:
          return "Please mention the employee name along with the department to proceed."
    match(intent):
        case 'CHECK':
            return getEmployee(name,department, db)
        case 'CREATE':
            return createEmployee(name,department, db)
        case 'UPDATE':
            if not updateField or not newValue:
                return "Please specify what to update and the new value"
            return updateEmployee(name, department, updateField, newValue, db)
        case 'DELETE':
            return deleteEmployee(name,department, db)
    return "Unknown intent"

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


@chat.post("/chat/file")
async def upload_file(
    file: UploadFile = File(...),
    userInput: str = Form(""),
    db: Session = Depends(get_db)
):

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only Pdfs supported")
    try:
        file_bytes = await file.read()
        content = extract_text_from_pdf(file_bytes)
        llm_response = get_api_response_for_attachment(content, userInput)
        print(llm_response)
        jsonResp = json.loads(llm_response)
        parsed = LLMResponseSchemaForInput(**jsonResp)

        result = proceed(
            parsed.intent,
            parsed.name,
            parsed.department,
            parsed.updateField,
            parsed.newValue,
            db,
        )

        return {"response": result}

    except Exception:
        return {"response": "Failed to process resume"}

    finally:
        await file.close()




