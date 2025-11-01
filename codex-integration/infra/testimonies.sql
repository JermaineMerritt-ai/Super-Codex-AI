CREATE TABLE testimonies (
  id UUID PRIMARY KEY,
  run_id UUID,
  capsule_id TEXT,
  level TEXT,
  message TEXT,
  created_at TIMESTAMP DEFAULT now()
);
