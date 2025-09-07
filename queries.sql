-- Total registrations per event
SELECT e.id AS event_id, e.title, COUNT(r.id) AS registrations
FROM events e
LEFT JOIN registrations r ON r.event_id = e.id
GROUP BY e.id, e.title
ORDER BY registrations DESC;

-- Attendance percentage per event
SELECT e.id AS event_id, e.title,
  (SUM(CASE WHEN a.present = 1 THEN 1 ELSE 0 END) * 100.0) / 
  NULLIF(COUNT(a.id),0) AS attendance_percent
FROM events e
LEFT JOIN registrations r ON r.event_id = e.id
LEFT JOIN attendance a ON a.registration_id = r.id
GROUP BY e.id, e.title
ORDER BY attendance_percent DESC;

-- Average feedback score per event
SELECT e.id AS event_id, e.title, AVG(f.rating) AS avg_feedback
FROM events e
LEFT JOIN registrations r ON r.event_id = e.id
LEFT JOIN feedback f ON f.registration_id = r.id
GROUP BY e.id, e.title
ORDER BY avg_feedback DESC;

-- Top 3 most active students by attended events
SELECT s.id AS student_id, s.name, COUNT(a.id) AS attended_events
FROM students s
JOIN registrations r ON r.student_id = s.id
JOIN attendance a ON a.registration_id = r.id AND a.present = 1
GROUP BY s.id, s.name
ORDER BY attended_events DESC
LIMIT 3;
