CREATE TABLE replay_queue (
  id UUID PRIMARY KEY,
  run_id UUID,
  flow_id TEXT,
  status TEXT DEFAULT 'pending',
  attempts INT DEFAULT 0,
  last_error TEXT,
  payload JSONB,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE impact_metrics (
  id UUID PRIMARY KEY,
  run_id UUID,
  flow_id TEXT,
  actions_executed INT,
  contributors_count INT,
  approvals_requested INT,
  created_at TIMESTAMP DEFAULT now()
);
