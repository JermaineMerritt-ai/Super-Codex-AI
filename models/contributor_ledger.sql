-- ✦ Contributor Recognition Ledger Schema
-- Purpose: Track credits, payouts, and lineage badges for all Capsule participants.

CREATE TABLE contributors (
    contributor_id      SERIAL PRIMARY KEY,
    name                VARCHAR(255) NOT NULL,
    role                VARCHAR(50) CHECK (role IN ('signal_author','validator','executor','custodian')),
    join_date           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status              VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE credits (
    credit_id           SERIAL PRIMARY KEY,
    contributor_id      INT REFERENCES contributors(contributor_id),
    capsule_id          VARCHAR(100) NOT NULL,
    signal_id           VARCHAR(100),
    weight_signal       NUMERIC(5,4) DEFAULT 0.0,
    weight_validation   NUMERIC(5,4) DEFAULT 0.0,
    weight_execution    NUMERIC(5,4) DEFAULT 0.0,
    total_credits       NUMERIC(10,4) GENERATED ALWAYS AS 
                        (weight_signal + weight_validation + weight_execution) STORED,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payouts (
    payout_id           SERIAL PRIMARY KEY,
    contributor_id      INT REFERENCES contributors(contributor_id),
    capsule_id          VARCHAR(100) NOT NULL,
    period_start        DATE NOT NULL,
    period_end          DATE NOT NULL,
    total_credits       NUMERIC(10,4) NOT NULL,
    payout_amount_usd   NUMERIC(12,2) NOT NULL,
    distributed_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lineage_badges (
    badge_id            SERIAL PRIMARY KEY,
    contributor_id      INT REFERENCES contributors(contributor_id),
    capsule_id          VARCHAR(100) NOT NULL,
    badge_type          VARCHAR(50) CHECK (badge_type IN ('founder','custodian','signal_master','validator_guard','executor_champion')),
    description         TEXT,
    awarded_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_contributors_role ON contributors(role);
CREATE INDEX idx_credits_capsule ON credits(capsule_id);
CREATE INDEX idx_payouts_capsule ON payouts(capsule_id);
CREATE INDEX idx_badges_capsule ON lineage_badges(capsule_id);
