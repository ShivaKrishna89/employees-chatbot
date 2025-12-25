from db.db import base
from sqlalchemy import Column,Integer,String

class UserBase(base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    department = Column(String(30))
    


