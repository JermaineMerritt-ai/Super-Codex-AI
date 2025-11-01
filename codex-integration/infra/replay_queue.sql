CREATE TABLE replay_queue (
    id SERIAL PRIMARY KEY,
    source TEXT,
    event_type TEXT,
    payload JSONB,
    status TEXT DEFAULT 'pending',
    attempts INT DEFAULT 0,
    last_error TEXT,
    created_at TIMESTAMP DEFAULT now()
);
