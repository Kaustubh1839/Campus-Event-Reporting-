from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from src.db import Base
import datetime

class College(Base):
    __tablename__ = 'colleges'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey('colleges.id'))
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    college = relationship('College')

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey('colleges.id'))
    title = Column(String, nullable=False)
    type = Column(String, nullable=True)
    date = Column(String, nullable=True)
    college = relationship('College')

class Registration(Base):
    __tablename__ = 'registrations'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    event_id = Column(Integer, ForeignKey('events.id'))
    registered_at = Column(DateTime, default=datetime.datetime.utcnow)

class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(Integer, ForeignKey('registrations.id'))
    present = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(Integer, ForeignKey('registrations.id'))
    rating = Column(Integer)
    comment = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
