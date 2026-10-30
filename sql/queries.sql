-- 1. All services
SELECT * FROM services;

-- 2. Title and severity of every open incident
SELECT title, severity FROM incidents WHERE status = 'open';

-- 3. Critical incidents, newest first
SELECT * FROM incidents WHERE severity = 'critical' ORDER BY created_at DESC;

-- 4. Titles containing "login", ignoring case
SELECT * FROM incidents WHERE title ILIKE '%login%';

-- 5. Open incidents with one of the top two severities
SELECT * FROM incidents
WHERE status = 'open' AND severity IN ('critical', 'high');

-- 6. Not yet resolved
SELECT * FROM incidents WHERE resolved_at IS NULL;

-- 7. Total incidents
SELECT count(*) FROM incidents;

-- 8. Every incident with its service name
SELECT i.id, i.title, s.name AS service_name
FROM incidents i
JOIN services s ON s.id = i.service_id;

-- 9. Incidents per service
SELECT s.name, count(*) AS incident_count
FROM services s
JOIN incidents i ON i.service_id = s.id
GROUP BY s.name;

-- 10. Only services with more than 2 incidents
SELECt s.name, count(*) AS incident_count
FROM services s
JOIN incidents i ON i.service_id = s.id
GROUP BY s.name
HAVING count(*) > 2;

-- 11. Open incidents per service, highest first
SELECt s.name, count(*) AS incident_count
FROM services s
JOIN incidents i ON i.service_id = s.id
WHERE i.status = 'open'
GROUP BY s.name
ORDER BY incident_count DESC;

-- 12. Service with zero incidents
SELECT s.name
FROM services s
LEFT JOIN incidents i ON i.service_id = s.id
WHERE i.id is NULL;