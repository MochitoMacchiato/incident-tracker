DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS services;

CREATE TABLE services(
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL UNIQUE,
    created_at timestamptz NOT NULL DEFAULT now() 
);

CREATE TABLE incidents(
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    service_id integer NOT NULL REFERENCES services (id),
    title text NOT NULL,
    severity text NOT NULL,
    status text NOT NULL DEFAULT 'open',
    created_at timestamptz NOT NULL DEFAULT now(),
    resolved_at timestamptz
);

CREATE INDEX idx_incidents_service_id ON incidents (service_id);
CREATE INDEX idx_incidents_status ON incidents (status);
