from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateTicket(BaseModel):
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: str

class UpdateTicket(BaseModel):
    status: Optional[str] = None
    note: Optional[str] = None
