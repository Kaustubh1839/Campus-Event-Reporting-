# Design Document - Campus Event Reporting System

## Assumptions & Decisions (brief)
- Use a single global database (SQLite) for simplicity.
- Event IDs are unique globally (UUID-like incremental integer works here).
- Keep data in one dataset (easier for reporting across colleges).
- Minimal auth (not required by assignment) — endpoints are open for demo.
- Scale assumption supported by schema; SQLite chosen for prototype.

## Data to Track
- Colleges, Students, Events, Registrations, Attendance, Feedback

## Database Schema (tables)
- colleges (id, name)
- students (id, college_id, name, email)
- events (id, college_id, title, type, date)
- registrations (id, student_id, event_id, registered_at)
- attendance (id, registration_id, present, timestamp)
- feedback (id, registration_id, rating, comment, timestamp)

### Mermaid ER (simple)
```
erDiagram
    COLLEGES ||--o{ STUDENTS : has
    COLLEGES ||--o{ EVENTS : organizes
    STUDENTS ||--o{ REGISTRATIONS : registers
    EVENTS ||--o{ REGISTRATIONS : has
    REGISTRATIONS ||--o{ ATTENDANCE : has
    REGISTRATIONS ||--o{ FEEDBACK : has
```

## API Design (minimal)
- `POST /events` - create event
- `POST /students` - create student
- `POST /register` - register student to event
- `POST /attendance` - mark attendance for a registration
- `POST /feedback` - submit feedback for a registration
- `GET /reports/registrations` - total registrations per event
- `GET /reports/attendance` - attendance percentage per event
- `GET /reports/feedback` - average feedback score per event
- `GET /reports/top-students` - top 3 active students (by attendance)

## Workflows (text)
1. Admin creates event (`POST /events`).
2. Student created (`POST /students`) or exists.
3. Student registers (`POST /register`).
4. On event day, attendance marked (`POST /attendance`).
5. After event, student submits feedback (`POST /feedback`).
6. Reports endpoints summarize data.

## Edge cases & Handling
- Duplicate registrations: API returns existing registration if attempted twice.
- Missing feedback: report averages consider only existing feedbacks.
- Cancelled events: not implemented (would add `cancelled` flag).
- Multiple attendance marks: latest overwrites previous.

