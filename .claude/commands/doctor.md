# /doctor
Project health check. Run before starting a new session or before /deploy.

## Checks
1. Environment
   - .env.local exists and has required keys (ANTHROPIC_API_KEY, SUPABASE_URL, SUPABASE_KEY)
   - Python venv active: apps/worker/.venv/
   - Node modules installed: apps/web/node_modules/

2. Database
   - Supabase reachable (supabase status)
   - All migrations applied (supabase db diff → should be empty)
   - No stuck ingestion_queue rows (status = 'processing' for > 1h)

3. Pipeline
   - pytest passing: cd apps/worker && pytest -q
   - TypeScript clean: cd apps/web && npx tsc --noEmit

4. Queue
   - Papers pending enrichment: SELECT count(*) FROM ingestion_queue WHERE status='pending'
   - Papers flagged for review: SELECT count(*) FROM enrichments WHERE enrichment_status='needs_review'

## Report format
✓ / ✗ per check + actionable fix for each failure
