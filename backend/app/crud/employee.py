from sqlalchemy.orm import Session
from db.db import session
from fastapi import Depends
from model.employee import UserBase




def getEmployee(name:str,department:str|None,db:Session):
  if department is not None:
    result = db.query(UserBase).filter(UserBase.name==name,UserBase.department==department).first()
  else:
    result = db.query(UserBase).filter(UserBase.name==name).first()

  return "Employee Not Exist" if result is None else "Employee Exist"


def createEmployee(name:str,department:str|None,db:Session):
  try:
    user = UserBase(name=name, department=department)
    db.add(user)
    db.commit()
    resp = "Employee has been Created"
  except Exception as e:
    db.rollback()
    resp = "Employee is not created - "+str(e)
  return resp

def updateEmployee(name:str, department:str, updateField:str,newValue:str, db:Session):
  try:
    user = db.query(UserBase).filter(UserBase.name==name, UserBase.department==department).first()
    if user is None:
      resp = "No Employee exist to update"
    else:
      if updateField == 'name':
        user.name = newValue
        resp = "Updated employee name"
        db.commit()
      elif updateField == 'department':
        user.department = newValue
        db.commit()
        resp = "Updated employee department"
      else:
        resp = 'Please give update field'
  except Exception as e:
    db.rollback()
    resp = "Employee is not updated - "+str(e)
  return resp


def deleteEmployee(name:str,department:str|None,db:Session):
  try:
    user = db.query(UserBase).filter(UserBase.name==name, UserBase.department==department).first()
    if user is None:
      resp = "No Employee exist to update"
    else:
      db.delete(user)
      db.commit()
      resp = "Employee has been Deleted"
  except Exception as e:
    db.rollback()
    resp = "Employee is not deleted  - "+str(e)
  return resp
