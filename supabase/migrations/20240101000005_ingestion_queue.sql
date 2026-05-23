CREATE TABLE ingestion_queue (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  raw        jsonb NOT NULL,
  source     text,
  status     text DEFAULT 'pending',
  error      text,
  created_at timestamptz DEFAULT now()
);

CREATE INDEX ON ingestion_queue (status);
CREATE INDEX ON ingestion_queue (created_at DESC);
