import { Suspense } from 'react'
import { createClient } from '@/lib/supabase/server'
import { FeedList } from '@/components/feed/FeedList'
import { FilterBar } from '@/components/feed/FilterBar'
import type { Paper, Enrichment, PaperWithEnrichment } from '@/types/supabase'

interface Props {
  searchParams: Promise<{
    sport?: string
    topic?: string
    region?: string
    search?: string
  }>
}

async function TopPicksFeed({
  sport,
  topic,
  region,
  search,
}: {
  sport?: string
  topic?: string
  region?: string
  search?: string
}) {
  const supabase = await createClient()

  // Query from enrichments side so we can sort by evidence_level (highest quality first)
  let query = supabase
    .from('enrichments')
    .select('*, papers!inner(*)')
    .eq('enrichment_status', 'auto_committed')
    .not('evidence_level', 'is', null)
    .order('evidence_level', { ascending: true })
    .order('created_at', { ascending: false })
    .limit(20)

  if (sport) query = query.contains('sports', [sport])
  if (topic) query = query.contains('topics', [topic])
  if (region) query = query.contains('body_regions', [region])
  if (search) query = query.ilike('papers.title', `%${search}%`)

  const { data, error } = await query

  if (error) {
    return <p className="text-red-500 text-sm">Failed to load papers: {error.message}</p>
  }

  // Transform enrichment-first rows into PaperWithEnrichment shape
  const papers: PaperWithEnrichment[] = (data ?? []).map((row) => {
    const { papers: paper, ...enrichment } = row as Enrichment & { papers: Paper }
    return { ...paper, enrichments: [enrichment] }
  })

  return <FeedList papers={papers} />
}

export default async function ForYouPage({ searchParams }: Props) {
  const { sport, topic, region, search } = await searchParams

  return (
    <main className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-1">Top Picks</h1>
      <p className="text-sm text-gray-500 mb-6">Highest-quality studies sorted by evidence level — RCTs and meta-analyses first</p>
      <Suspense>
        <FilterBar />
      </Suspense>
      <Suspense fallback={<p className="text-gray-400 text-sm">Loading&hellip;</p>}>
        <TopPicksFeed sport={sport} topic={topic} region={region} search={search} />
      </Suspense>
    </main>
  )
}
