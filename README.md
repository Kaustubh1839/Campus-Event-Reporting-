# Campus Event Management - Reporting System

## Problem
A simple system to manage campus events where admins create events and students register, mark attendance, and submit feedback (1-5). The goal is to generate basic reports: registrations, attendance percentage, and average feedback.

## Approach
Built a minimal backend using FastAPI + SQLite. Includes endpoints for creating events/students, registering, marking attendance, and submitting feedback. A seed script populates sample data so reports work immediately.

## How to run (quick)
1. Create virtual env and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Seed sample data (creates sqlite DB):
   ```bash
   python src/seed.py
   ```
3. Run the API:
   ```bash
   uvicorn src.app:app --reload
   ```
4. Open API docs: http://127.0.0.1:8000/docs

## Expected output
- Working endpoints with sample data. Use `/reports/*` endpoints to fetch required reports.
- The repo includes `design_document.md`, `reports/queries.sql`, and `ai_conversation_log.md` for submission.

