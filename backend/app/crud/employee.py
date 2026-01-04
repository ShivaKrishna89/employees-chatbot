from sqlalchemy.orm import Session
from db.db import session
from fastapi import Depends
from model.employee import UserBase




def getEmployee(name:str,department:str|None,db:Session):
  if department is not None:
    result = db.query(UserBase).filter(UserBase.name==name,UserBase.department==department).first()
  else:
    result = db.query(UserBase).filter(UserBase.name==name).first()

  return f"Employee {name} doesnot exists in the {department} department." if result is None else f"Employee {name} exists in the {department} department."


def createEmployee(name:str,department:str|None,db:Session):
  try:
    user = UserBase(name=name, department=department)
    result = db.query(UserBase).filter(UserBase.name==name,UserBase.department==department).first()
    if result:
      resp = f"Employee {name} already exists in the {department} department."
    else:
      db.add(user)
      db.commit()
      resp = f"Employee {name} has been created in the {department} department."
  except Exception as e:
    db.rollback()
    resp = "Employee is not created - "+str(e)
  return resp

def updateEmployee(name:str, department:str, updateField:str,newValue:str, db:Session):
  try:
    user = db.query(UserBase).filter(UserBase.name==name, UserBase.department==department).first()
    if user is None:
      resp = f"No Employee with {name} in the {department} department exist."
    else:
      if updateField == 'name':
        user.name = newValue
        resp = f"Updated the employee name from {name} to {newValue} in the {department} department."
        db.commit()
      elif updateField == 'department':
        user.department = newValue
        db.commit()
        resp = f"Updated the employee department from {department} to {newValue} for {name}."
  except Exception as e:
    db.rollback()
    resp = "Employee is not updated - "+str(e)
  return resp


def deleteEmployee(name:str,department:str|None,db:Session):
  try:
    user = db.query(UserBase).filter(UserBase.name==name, UserBase.department==department).first()
    if user is None:
      resp = f"No Employee with {name} in the {department} department exist."
    else:
      db.delete(user)
      db.commit()
      resp = f"Employee with {name} in the {department} department has been deleted."
  except Exception as e:
    db.rollback()
    resp = "Employee is not deleted  - "+str(e)
  return resp
