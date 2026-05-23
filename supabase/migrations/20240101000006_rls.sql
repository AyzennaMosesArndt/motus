-- Grant table-level privileges (required for PostgREST access alongside RLS)
GRANT SELECT ON papers TO authenticated, anon;
GRANT SELECT ON enrichments TO authenticated, anon;
GRANT SELECT, INSERT, UPDATE ON users TO authenticated;
GRANT SELECT, INSERT, DELETE ON saves TO authenticated;
GRANT ALL ON ingestion_queue TO service_role;
GRANT USAGE ON SCHEMA public TO authenticated, anon, service_role;

ALTER TABLE papers ENABLE ROW LEVEL SECURITY;
ALTER TABLE enrichments ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE saves ENABLE ROW LEVEL SECURITY;
ALTER TABLE ingestion_queue ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read papers"
  ON papers FOR SELECT TO authenticated
  USING (true);

CREATE POLICY "public read enrichments"
  ON enrichments FOR SELECT TO authenticated
  USING (true);

CREATE POLICY "users read own row"
  ON users FOR SELECT TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "users insert own row"
  ON users FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = id);

CREATE POLICY "users update own row"
  ON users FOR UPDATE TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "users read own saves"
  ON saves FOR SELECT TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "users write own saves"
  ON saves FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "users delete own saves"
  ON saves FOR DELETE TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "service role ingestion_queue"
  ON ingestion_queue FOR ALL TO service_role
  USING (true)
  WITH CHECK (true);

-- Allow anon/unauthenticated users to browse papers + enrichments (public discovery)
CREATE POLICY "anon read papers"
  ON papers FOR SELECT TO anon
  USING (true);

CREATE POLICY "anon read enrichments"
  ON enrichments FOR SELECT TO anon
  USING (true);
