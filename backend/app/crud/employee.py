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


def CreateEmployee(name:str,department:str|None,db:Session):
  try:
    user = UserBase(name=name, department=department)
    db.add(user)
    db.commit()
    resp = "Employee has been Created"
  except Exception as e:
    db.rollback()
    resp = "Employee is not created - "+str(e)
  return resp
