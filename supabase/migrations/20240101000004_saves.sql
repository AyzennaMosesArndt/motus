CREATE TABLE saves (
  id        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id   uuid REFERENCES users(id) ON DELETE CASCADE,
  paper_id  uuid REFERENCES papers(id) ON DELETE CASCADE,
  list_name text DEFAULT 'default',
  saved_at  timestamptz DEFAULT now(),
  UNIQUE(user_id, paper_id)
);

CREATE INDEX ON saves (user_id, list_name);
CREATE INDEX ON saves (paper_id);
