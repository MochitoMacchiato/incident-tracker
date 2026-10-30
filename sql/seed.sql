INSERT INTO services (name) VALUES
    ('api-gateway'),
    ('payments'),
    ('auth'),
    ('reporting');



INSERT INTO incidents (service_id, title, severity, status, created_at, resolved_at) VALUES
    (1, 'API latency spike',           'high',     'resolved', '2026-10-01 09:00', '2026-10-01 11:30'),
    (1, 'Gateway 502 errors',          'critical', 'open',     '2026-10-20 14:10', NULL),
    (1, 'TLS certificate expiring',    'medium',   'resolved', '2026-10-05 08:00', '2026-10-05 10:00'),
    (1, 'Rate limiter misconfigured',  'low',      'open',     '2026-10-22 16:00', NULL),
    (2, 'Payment timeout',             'critical', 'resolved', '2026-10-03 13:00', '2026-10-03 15:45'),
    (2, 'Duplicate charge reports',    'high',     'open',     '2026-10-25 10:20', NULL),
    (2, 'Slow checkout page',          'medium',   'open',     '2026-10-27 09:30', NULL),
    (2, 'Refund job failing',          'high',     'resolved', '2026-10-10 07:00', '2026-10-11 12:00'),
    (2, 'Webhook retries piling up',   'low',      'resolved', '2026-10-15 18:00', '2026-10-16 09:00'),
    (3, 'Login failures after deploy', 'critical', 'resolved', '2026-10-08 11:00', '2026-10-08 12:15'),
    (3, 'Password reset email delayed','medium',   'open',     '2026-10-28 08:45', NULL),
    (3, 'Session token expiry bug',    'high',     'resolved', '2026-10-18 15:30', '2026-10-19 10:00'),
    (3, 'Slow login on mobile',        'low',      'open',     '2026-10-29 12:00', NULL);