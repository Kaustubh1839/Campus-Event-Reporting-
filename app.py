from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.db import SessionLocal, engine, Base
from src import models, schemas
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Depends

Base.metadata.create_all(bind=engine)
app = FastAPI(title='Campus Event Reporting API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/events', response_model=schemas.EventOut)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = models.Event(**event.dict())
    db.add(db_event); db.commit(); db.refresh(db_event)
    return db_event

@app.post('/students', response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student); db.commit(); db.refresh(db_student)
    return db_student

@app.post('/register', response_model=schemas.RegistrationOut)
def register(reg: schemas.RegistrationCreate, db: Session = Depends(get_db)):
    # prevent duplicate registration
    existing = db.query(models.Registration).filter_by(student_id=reg.student_id, event_id=reg.event_id).first()
    if existing:
        return existing
    new = models.Registration(student_id=reg.student_id, event_id=reg.event_id, registered_at=datetime.utcnow())
    db.add(new); db.commit(); db.refresh(new)
    return new

@app.post('/attendance', response_model=schemas.AttendanceOut)
def mark_attendance(att: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    reg = db.query(models.Registration).filter_by(id=att.registration_id).first()
    if not reg:
        raise HTTPException(404, 'Registration not found')
    # upsert attendance (one per registration)
    existing = db.query(models.Attendance).filter_by(registration_id=att.registration_id).first()
    if existing:
        existing.present = att.present
        existing.timestamp = datetime.utcnow()
        db.commit(); db.refresh(existing)
        return existing
    new = models.Attendance(registration_id=att.registration_id, present=att.present, timestamp=datetime.utcnow())
    db.add(new); db.commit(); db.refresh(new)
    return new

@app.post('/feedback', response_model=schemas.FeedbackOut)
def submit_feedback(fd: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    reg = db.query(models.Registration).filter_by(id=fd.registration_id).first()
    if not reg:
        raise HTTPException(404, 'Registration not found')
    new = models.Feedback(registration_id=fd.registration_id, rating=fd.rating, comment=fd.comment, timestamp=datetime.utcnow())
    db.add(new); db.commit(); db.refresh(new)
    return new

# Reports
from sqlalchemy import func, case



@app.get('/reports/registrations')
def report_registrations(db: Session = Depends(get_db)):
    q = db.query(models.Event.id, models.Event.title, func.count(models.Registration.id).label('registrations')).        outerjoin(models.Registration, models.Registration.event_id==models.Event.id).        group_by(models.Event.id, models.Event.title).order_by(func.count(models.Registration.id).desc()).all()
    return [{'event_id': r[0], 'title': r[1], 'registrations': r[2]} for r in q]

@app.get('/reports/attendance')
def report_attendance(db: Session = Depends(get_db)):
    a_count = func.sum(case([(models.Attendance.present==1,1)], else_=0))
    total = func.count(models.Attendance.id)
    q = db.query(models.Event.id, models.Event.title, (a_count * 100.0) / func.nullif(total, 0)
).        outerjoin(models.Registration, models.Registration.event_id==models.Event.id).        outerjoin(models.Attendance, models.Attendance.registration_id==models.Registration.id).        group_by(models.Event.id, models.Event.title).all()
    return [{'event_id': r[0], 'title': r[1], 'attendance_percent': float(r[2] or 0)} for r in q]

@app.get('/reports/feedback')
def report_feedback(db: Session = Depends(get_db)):
    q = db.query(models.Event.id, models.Event.title, func.avg(models.Feedback.rating)).        outerjoin(models.Registration, models.Registration.event_id==models.Event.id).        outerjoin(models.Feedback, models.Feedback.registration_id==models.Registration.id).        group_by(models.Event.id, models.Event.title).all()
    return [{'event_id': r[0], 'title': r[1], 'avg_feedback': float(r[2] or 0)} for r in q]

@app.get('/reports/top-students')
def report_top_students(limit: int = 3, db: Session = Depends(get_db)):
    q = db.query(models.Student.id, models.Student.name, func.count(models.Attendance.id).label('attended')).        join(models.Registration, models.Registration.student_id==models.Student.id).        join(models.Attendance, models.Attendance.registration_id==models.Registration.id).        filter(models.Attendance.present==1).        group_by(models.Student.id, models.Student.name).order_by(func.count(models.Attendance.id).desc()).limit(limit).all()
    return [{'student_id': r[0], 'name': r[1], 'attended': r[2]} for r in q]
