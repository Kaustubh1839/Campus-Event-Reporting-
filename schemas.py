from pydantic import BaseModel
from typing import Optional

class EventCreate(BaseModel):
    college_id: int
    title: str
    type: Optional[str] = None
    date: Optional[str] = None

class EventOut(EventCreate):
    id: int
    class Config:
        orm_mode = True

class StudentCreate(BaseModel):
    college_id: int
    name: str
    email: Optional[str] = None

class StudentOut(StudentCreate):
    id: int
    class Config:
        orm_mode = True

class RegistrationCreate(BaseModel):
    student_id: int
    event_id: int

class RegistrationOut(RegistrationCreate):
    id: int
    registered_at: Optional[str] = None
    class Config:
        orm_mode = True

class AttendanceCreate(BaseModel):
    registration_id: int
    present: bool

class AttendanceOut(AttendanceCreate):
    id: int
    timestamp: Optional[str] = None
    class Config:
        orm_mode = True

class FeedbackCreate(BaseModel):
    registration_id: int
    rating: int
    comment: Optional[str] = None

class FeedbackOut(FeedbackCreate):
    id: int
    timestamp: Optional[str] = None
    class Config:
        orm_mode = True
