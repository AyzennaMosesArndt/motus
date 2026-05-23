CREATE TABLE enrichments (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  paper_id            uuid NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
  summary             text,
  tags                text[],
  sports              text[],
  body_regions        text[],
  topics              text[],
  evidence_level      int CHECK (evidence_level BETWEEN 1 AND 4),
  study_type          text,
  sample_size         int,
  population          text,
  practical_relevance boolean DEFAULT true,
  confidence_sports   float CHECK (confidence_sports BETWEEN 0 AND 1),
  confidence_regions  float CHECK (confidence_regions BETWEEN 0 AND 1),
  confidence_topics   float CHECK (confidence_topics BETWEEN 0 AND 1),
  confidence_evidence float CHECK (confidence_evidence BETWEEN 0 AND 1),
  enrichment_status   text DEFAULT 'pending'
                        CHECK (enrichment_status IN (
                          'pending','processing','auto_committed',
                          'needs_review','rejected','flagged','failed'
                        )),
  created_at          timestamptz DEFAULT now()
);

CREATE INDEX ON enrichments USING GIN (sports);
CREATE INDEX ON enrichments USING GIN (body_regions);
CREATE INDEX ON enrichments USING GIN (tags);
CREATE INDEX ON enrichments USING GIN (topics);
CREATE INDEX ON enrichments (enrichment_status);
CREATE INDEX ON enrichments (paper_id);
CREATE INDEX ON enrichments (evidence_level);
