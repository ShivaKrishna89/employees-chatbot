from pydantic import BaseModel
from typing import Optional

class EmployeeSchema(BaseModel):
    name: str | None
    department: str | None

class LLMResponseSchemaForInput(BaseModel):
    intent: str | None
    name: str | None
    department: str | None
    updateField: Optional[str] = None
    newValue: Optional[str] = None
