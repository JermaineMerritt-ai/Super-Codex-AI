-- flows
CREATE TABLE flows (
  id TEXT PRIMARY KEY,
  version INT NOT NULL,
  title TEXT,
  sector TEXT,
  owner TEXT,
  status TEXT DEFAULT 'draft',
  capsule JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

-- runs
CREATE TABLE runs (
  id UUID PRIMARY KEY,
  flow_id TEXT REFERENCES flows(id),
  status TEXT,
  context JSONB,
  created_at TIMESTAMP DEFAULT now()
);

-- testimonies
CREATE TABLE testimonies (
  id UUID PRIMARY KEY,
  run_id UUID REFERENCES runs(id),
  capsule_id TEXT,
  level TEXT,
  message TEXT,
  created_at TIMESTAMP DEFAULT now()
);
