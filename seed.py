from src.db import SessionLocal, engine, Base
from src import models
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Clear existing (for repeatable seed)
db.query(models.Feedback).delete()
db.query(models.Attendance).delete()
db.query(models.Registration).delete()
db.query(models.Event).delete()
db.query(models.Student).delete()
db.query(models.College).delete()
db.commit()

# Seed colleges
c1 = models.College(name='College A')
c2 = models.College(name='College B')
db.add_all([c1,c2]); db.commit()
# Seed students
s1 = models.Student(college_id=c1.id, name='Alice', email='alice@example.com')
s2 = models.Student(college_id=c1.id, name='Bob', email='bob@example.com')
s3 = models.Student(college_id=c2.id, name='Charlie', email='charlie@example.com')
s4 = models.Student(college_id=c2.id, name='David', email='david@example.com')
s5 = models.Student(college_id=c1.id, name='Eve', email='eve@example.com')
db.add_all([s1,s2,s3,s4,s5]); db.commit()

# Seed events
e1 = models.Event(college_id=c1.id, title='Intro to ML', type='Workshop', date='2025-09-01')
e2 = models.Event(college_id=c1.id, title='Flutter Workshop', type='Workshop', date='2025-09-05')
e3 = models.Event(college_id=c2.id, title='Hackathon Kickoff', type='Hackathon', date='2025-09-10')
db.add_all([e1,e2,e3]); db.commit()

# Registrations
r1 = models.Registration(student_id=s1.id, event_id=e1.id)
r2 = models.Registration(student_id=s2.id, event_id=e1.id)
r3 = models.Registration(student_id=s3.id, event_id=e1.id)
r4 = models.Registration(student_id=s1.id, event_id=e2.id)
r5 = models.Registration(student_id=s4.id, event_id=e2.id)
r6 = models.Registration(student_id=s5.id, event_id=e3.id)
db.add_all([r1,r2,r3,r4,r5,r6]); db.commit()

# Attendance (present True/False)
a1 = models.Attendance(registration_id=r1.id, present=True)
a2 = models.Attendance(registration_id=r2.id, present=False)
a3 = models.Attendance(registration_id=r3.id, present=True)
a4 = models.Attendance(registration_id=r4.id, present=False)
a5 = models.Attendance(registration_id=r5.id, present=True)
a6 = models.Attendance(registration_id=r6.id, present=True)
db.add_all([a1,a2,a3,a4,a5,a6]); db.commit()

# Feedback
f1 = models.Feedback(registration_id=r1.id, rating=5, comment='Great')
f2 = models.Feedback(registration_id=r3.id, rating=3, comment='Okay')
f3 = models.Feedback(registration_id=r5.id, rating=4, comment='Good')
f4 = models.Feedback(registration_id=r6.id, rating=5, comment='Excellent')
db.add_all([f1,f2,f3,f4]); db.commit()

print('Seed complete. DB created at ./src/../db.sqlite')