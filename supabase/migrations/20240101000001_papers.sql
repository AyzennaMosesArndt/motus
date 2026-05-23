CREATE TABLE papers (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  doi          text UNIQUE,
  title        text NOT NULL,
  abstract     text,
  authors      text[],
  journal      text,
  source_url   text,
  source_id    text,
  source_name  text,
  published_at date,
  created_at   timestamptz DEFAULT now()
);

CREATE INDEX ON papers (published_at DESC);
CREATE INDEX ON papers (created_at DESC);
CREATE INDEX ON papers (doi) WHERE doi IS NOT NULL;
