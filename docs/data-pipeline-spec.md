# Data Pipeline Specification — Motus

This is the authoritative reference for all source clients.
Do not deviate from field mappings, rate limits, or query lists defined here.

---

## 1. SPORTS TAXONOMY

Platform covers exclusively endurance sports.
No gym/bodybuilding/team sports content.

### RUNNING
Subcategories:
- sprint — < 800m
- middle — 800m – 5K
- short — 5K – 10K
- half_marathon — 21.1km
- marathon — 42.2km
- ultra — > 42.2km, trail, mountain

### CYCLING
Subcategories:
- road — road racing, gran fondo
- track — velodrome
- gravel — gravel racing, bikepacking
- ultra — > 300km, ultra endurance

### ROWING
No subcategories.

### HYROX
No subcategories.

### INLINE_SKATING
No subcategories.

### SKIING
Subcategories:
- alpine — downhill, slalom
- cross_country — classic, skate skiing
- ski_touring — backcountry
- biathlon — ski + shooting

---

## 2. TOPIC TAXONOMY (internal — pipeline use only)

### PHYSIOLOGY
- vo2max — maximal oxygen uptake, aerobic capacity
- lactate — lactate threshold, LT1, LT2
- hrv — heart rate variability, autonomic nervous system
- cardiac_output — stroke volume, cardiac drift
- altitude — hypoxia, altitude training, acclimatization

### PERFORMANCE
- biomechanics — running economy, gait, stride, cadence, ground contact time, power output
- pacing — race strategy, even split, negative split
- heat_performance — thermoregulation, heat stress, cooling strategies
- fatigue — central fatigue, peripheral fatigue, neuromuscular

### TRAINING
- periodization — training blocks, taper, peaking, base building
- intervals — HIIT, tempo, threshold, fartlek, VO2max intervals
- strength — strength training for endurance, plyometrics, resistance training
- overtraining — overreaching, RED-S, non-functional overreaching

### RECOVERY
- sleep — sleep quality, duration, napping, chronotype
- active_recovery — easy running, cross-training, recovery rides
- passive_recovery — rest, massage, compression, ice bath, sauna
- hrv_recovery — HRV-guided training, readiness scores

### NUTRITION
- carbohydrates — glycogen, fueling, carbohydrate loading, race nutrition, gels
- protein — muscle protein synthesis, recovery nutrition, timing
- hydration — sweat rate, electrolytes, hyponatremia, fluid intake
- supplements — caffeine, beta-alanine, creatine, nitrates, bicarbonate
- gut_health — GI distress, runner's gut, microbiome, intestinal permeability

### INJURY
- tendon — achilles tendinopathy, patellar tendinopathy, tendon loading
- stress_fracture — bone stress injury, metatarsal, tibial
- it_band — iliotibial band syndrome, lateral knee pain
- plantar_fascia — plantar fasciitis, heel pain
- knee — patellofemoral syndrome, runner's knee
- hamstring — hamstring strain, proximal hamstring
- prevention — injury prevention, load management, return to running

### MENTAL
- psychology — mental toughness, self-efficacy, motivation
- pacing_strategy — psychological aspects of pacing
- pain_tolerance — perceived exertion, RPE, pain management

---

## 3. FRONTEND TOPIC MAPPING
(internal topics → user-facing filter labels)

| Frontend Label | Internal Topics |
|----------------|-----------------|
| Recovery | sleep, active_recovery, passive_recovery, hrv_recovery |
| Nutrition | carbohydrates, protein, hydration, supplements, gut_health |
| Injury | tendon, stress_fracture, it_band, plantar_fascia, knee, hamstring, prevention |
| VO2max | vo2max, lactate, cardiac_output |
| Biomechanics | biomechanics, pacing, fatigue |
| Training | periodization, intervals, strength, overtraining |
| HRV | hrv, hrv_recovery |
| Sleep | sleep |
| Altitude | altitude |
| Heat | heat_performance |
| Psychology | psychology, pain_tolerance, pacing_strategy |

---

## 4. BODY REGIONS TAXONOMY

### LOWER LEG
- calves — gastrocnemius, soleus
- achilles — achilles tendon
- ankles — ankle stability, dorsiflexion
- foot — plantar fascia, metatarsals

### UPPER LEG
- quads — quadriceps, rectus femoris
- hamstrings — biceps femoris, semitendinosus
- it_band — iliotibial band, TFL
- knees — patellofemoral, MCL, LCL

### HIP + GLUTES
- glutes — gluteus maximus, medius, minimus
- hip_flexors — iliopsoas, rectus femoris
- hip_abductors — gluteus medius, TFL

### CORE + BACK
- core — transverse abdominis, obliques, rectus abdominis
- lower_back — lumbar spine, erector spinae

### UPPER BODY
- shoulders — rotator cuff, deltoids
- neck — cervical, trapezius
- grip_forearms — forearm flexors, grip strength
- lats — latissimus dorsi (rowing focus)

---

## 5. SPORT → BODY REGION MAPPING
(used by tagger to validate body_region tags)

### running
- primary: calves, quads, hamstrings, glutes, core, achilles, knees, foot
- injury: achilles, knees, it_band, plantar_fascia, foot

### cycling
- primary: quads, hip_flexors, lower_back, knees, neck, glutes
- injury: knees, lower_back, neck, hip_flexors

### rowing
- primary: lats, core, quads, lower_back, grip_forearms, shoulders
- injury: lower_back, knees, grip_forearms

### hyrox
- primary: shoulders, lower_back, knees, grip_forearms, core, quads
- injury: shoulders, lower_back, knees

### skiing
- primary: quads, core, hip_flexors, ankles, glutes, lower_back
- injury: knees, ankles, lower_back

### inline_skating
- primary: quads, glutes, hip_abductors, core, ankles
- injury: ankles, knees, hip_abductors

---

## 6. EVIDENCE LEVEL DEFINITIONS

| Level | Name | Includes |
|-------|------|----------|
| 1 | HIGH EVIDENCE | RCT, Meta-analysis, Systematic review of RCTs |
| 2 | MODERATE EVIDENCE | Cohort study, Controlled trial (non-randomized), Cross-sectional (large N) |
| 3 | LIMITED EVIDENCE | Case study/series, Expert opinion with data, Cross-sectional (small N < 20) |
| 4 | MECHANISTIC / DESCRIPTIVE | Mechanistic study, Narrative review, Editorial/commentary, Biomechanical modeling |

---

## 7. PUBMED SEARCH QUERIES (65 total)

All queries:
- Use [TIAB] field (title + abstract)
- Append: AND ("2018/01/01"[PDAT] : "3000"[PDAT])
- Max results per query: 50
- Deduplicate by DOI across all queries

### RUNNING (10 queries)
```
"endurance running"[TIAB]
"distance running"[TIAB]
"marathon running"[TIAB]
"ultramarathon"[TIAB]
"trail running"[TIAB]
"running economy"[TIAB]
"running biomechanics"[TIAB]
"sprint performance"[TIAB] AND "running"[TIAB]
"5K performance"[TIAB] OR "10K performance"[TIAB]
"half marathon"[TIAB] AND "performance"[TIAB]
```

### CYCLING (7 queries)
```
"endurance cycling"[TIAB]
"road cycling"[TIAB] AND "performance"[TIAB]
"cycling power output"[TIAB]
"track cycling"[TIAB] AND "physiology"[TIAB]
"gravel cycling"[TIAB]
"ultra cycling"[TIAB]
"cyclist physiology"[TIAB]
```

### ROWING (5 queries)
```
"rowing performance"[TIAB]
"ergometer rowing"[TIAB]
"indoor rowing"[TIAB]
"rowing biomechanics"[TIAB]
"sculling"[TIAB] AND "physiology"[TIAB]
```

### SKIING (5 queries)
```
"cross-country skiing"[TIAB]
"alpine skiing"[TIAB] AND "physiology"[TIAB]
"ski touring"[TIAB]
"biathlon"[TIAB] AND "performance"[TIAB]
"nordic skiing"[TIAB] AND "endurance"[TIAB]
```

### HYROX / FUNCTIONAL (5 queries)
```
"functional fitness"[TIAB]
"obstacle race"[TIAB]
"concurrent training"[TIAB]
"hybrid athlete"[TIAB]
"functional threshold"[TIAB]
```

### INLINE SKATING (3 queries)
```
"inline skating"[TIAB]
"speed skating"[TIAB] AND "endurance"[TIAB]
"roller skating"[TIAB] AND "physiology"[TIAB]
```

### PHYSIOLOGY cross-sport (8 queries)
```
"maximal oxygen uptake"[TIAB]
"VO2max"[TIAB] AND "endurance"[TIAB]
"lactate threshold"[TIAB]
"heart rate variability"[TIAB] AND "exercise"[TIAB]
"cardiac output"[TIAB] AND "exercise"[TIAB]
"altitude training"[TIAB]
"heat acclimatization"[TIAB] AND "exercise"[TIAB]
"anaerobic threshold"[TIAB]
```

### TRAINING (7 queries)
```
"periodization"[TIAB] AND "endurance"[TIAB]
"high intensity interval training"[TIAB]
"HIIT"[TIAB] AND "endurance"[TIAB]
"strength training"[TIAB] AND "endurance"[TIAB]
"training load"[TIAB] AND "endurance"[TIAB]
"taper"[TIAB] AND "endurance"[TIAB]
"overtraining"[TIAB] OR "RED-S"[TIAB]
```

### RECOVERY (7 queries)
```
"exercise recovery"[TIAB]
"sleep"[TIAB] AND "athletic performance"[TIAB]
"sleep quality"[TIAB] AND "athlete"[TIAB]
"HRV-guided training"[TIAB]
"cold water immersion"[TIAB] AND "exercise"[TIAB]
"compression garment"[TIAB] AND "recovery"[TIAB]
"sauna"[TIAB] AND "exercise recovery"[TIAB]
```

### NUTRITION (9 queries)
```
"endurance nutrition"[TIAB]
"carbohydrate loading"[TIAB]
"sports nutrition"[TIAB] AND "endurance"[TIAB]
"protein intake"[TIAB] AND "endurance"[TIAB]
"hydration"[TIAB] AND "exercise performance"[TIAB]
"caffeine"[TIAB] AND "endurance"[TIAB]
"beta-alanine"[TIAB] AND "performance"[TIAB]
"nitrate supplementation"[TIAB]
"gastrointestinal"[TIAB] AND "running"[TIAB]
```

### INJURY (9 queries)
```
"achilles tendinopathy"[TIAB]
"running injury"[TIAB]
"stress fracture"[TIAB] AND "running"[TIAB]
"iliotibial band"[TIAB]
"patellofemoral"[TIAB] AND "running"[TIAB]
"plantar fasciitis"[TIAB]
"hamstring injury"[TIAB] AND "running"[TIAB]
"injury prevention"[TIAB] AND "endurance"[TIAB]
"load management"[TIAB] AND "injury"[TIAB]
```

**Total: 65 queries**
Expected unique papers per run: 200–800

---

## 8. ARXIV SEARCH QUERIES (10 queries)

URL: `http://export.arxiv.org/api/query`
No key needed. Rate limit: 0.5s between requests.
Max results per query: 25

```
all:endurance running physiology
all:running biomechanics performance
all:cycling performance physiology
all:VO2max endurance training
all:sports nutrition endurance athlete
all:HRV heart rate variability exercise
all:running injury prevention biomechanics
all:marathon performance prediction
all:altitude training hypoxia endurance
all:strength training endurance performance
```

Note: arXiv is supplementary. Lower signal ratio than PubMed. Flag all: `source_name='arxiv'`

---

## 9. SEMANTIC SCHOLAR QUERIES (10 queries)

**LEER-ROHR: skip entirely if no API key.**
Rate limit: 1.1s between requests. Max per query: 50. Priority filter: citationCount > 5

```
endurance running performance
cycling physiology performance
VO2max training adaptation
sports nutrition endurance
running injury prevention
heart rate variability athletes
altitude training endurance
ultramarathon physiology
rowing performance biomechanics
strength training endurance athletes
```

---

## 10. RSS FEEDS (6 feeds)

### PRIMARY (high signal)
- BJSM: `https://bjsm.bmj.com/rss/current.xml`
- Journal of Applied Physiology: `https://journals.physiology.org/action/showFeed?type=etoc&feed=rss&jc=jappl`
- IJSNEM: `https://journals.humankinetics.com/rss/journals/ijsnem`
- European Journal of Sport Science: `https://www.tandfonline.com/action/showFeed?type=etoc&feed=rss&jc=tejs20`

### SECONDARY (moderate signal)
- Sports Medicine (Springer): `https://link.springer.com/search.rss?query=endurance+exercise&facet-journal-id=40279`
- Frontiers in Physiology: `https://www.frontiersin.org/journals/physiology/rss`

Poll: daily via GitHub Actions (06:00 UTC)

After RSS discovery:
1. Extract title + link + pubDate
2. Attempt DOI from link
3. If DOI: validate via crossref_client
4. Insert to ingestion_queue
5. Full metadata via pubmed title search

---

## 11. FIELD MAPPING — ALL SOURCES → papers table

Target fields: `doi, title, abstract, authors[], journal, source_url, source_id, source_name, published_at`

### PubMed → papers
```
ArticleId[@doi]           → doi
ArticleTitle              → title
AbstractText (join list)  → abstract
Author: LastName+ForeName → authors[]
Journal/Title             → journal
PMID                      → source_id
'pubmed'                  → source_name
PubDate Year+Month+Day    → published_at (ISO8601)
pubmed.ncbi.nlm.nih.gov/{pmid} → source_url
```

### Semantic Scholar → papers
```
externalIds.DOI           → doi
title                     → title
abstract                  → abstract
authors[].name            → authors[]
publicationVenue.name     → journal
paperId                   → source_id
'semantic_scholar'        → source_name
publicationDate           → published_at
semanticscholar.org/paper/{id} → source_url
```

### arXiv → papers
```
entry.arxiv_doi or None   → doi
entry.title (strip \n)    → title
entry.summary             → abstract
entry.authors[].name      → authors[]
'arXiv'                   → journal
entry.id                  → source_id
'arxiv'                   → source_name
entry.published           → published_at
entry.link                → source_url
```

### RSS + Crossref → papers
```
message.DOI               → doi
message.title[0]          → title
message.abstract or None  → abstract
message.author            → authors[]
message.container-title[0]→ journal
message.DOI               → source_id
'rss'                     → source_name
message.published         → published_at
feed_entry.link           → source_url
```

---

## 12. QUALITY FILTERS

### HARD REJECT (normalizer — status='failed')
- abstract is None
- word_count(abstract) < 80
- doi is None AND source_url is None
- published_at < 2018-01-01
- doi already in papers table (duplicate)
- md5(title.lower().strip()) already in papers (title hash duplicate)

### SOFT REJECT (tagger — kept but excluded from feed)
- all confidence scores < 0.60 → enrichment_status = 'rejected'
- any score 0.60–0.84 → enrichment_status = 'needs_review'
- no sport tag assigned → enrichment_status = 'flagged'

### AUTO-COMMIT (shown in feed)
- all confidence scores ≥ 0.85
- summary ≤ 120 words
- evidence_level not null
- ≥ 1 sport tag
- ≥ 1 topic tag

### PRIORITY BOOST (higher in feed)
- evidence_level IN (1, 2)
- sample_size > 20
- population IN ('trained', 'elite')
- source_name = 'pubmed'

---

## 13. RATE LIMITS SUMMARY

| Source | Delay | Notes |
|--------|-------|-------|
| PubMed (with API key) | 0.1s between requests | |
| PubMed (no key) | 0.35s between requests | |
| Semantic Scholar | 1.1s between requests | |
| arXiv | 0.5s between requests | |
| Crossref (polite) | 0.5s between requests | |
| RSS | poll max 1x/day per feed | |

Implement as `time.sleep()` in each client. Never batch-fire without delay.

---

## 14. RESEARCHER.PY — FULL QUERY PLAN

When `--source all`:

### STEP 1: PubMed (65 queries)
- For each query + DATE_FILTER: esearch → get PMIDs → efetch → get full records
- Normalize → insert to ingestion_queue if new
- Delay: 0.1s between requests
- Expected: 300–800 unique papers per run

### STEP 2: Semantic Scholar (skip if no key)
- For each of 10 queries: search → get papers
- Cross-reference DOIs with Step 1
- Insert only new papers
- Delay: 1.1s between requests

### STEP 3: arXiv (10 queries)
- For each query: fetch Atom XML → parse with feedparser
- Insert only new papers
- Delay: 0.5s between requests

### STEP 4: RSS (6 feeds)
- For each feed: fetch → parse entries → attempt DOI extraction → enrich via crossref_client
- Insert only new papers
- No delay needed (1x/day)

### STEP 5: End report (print to stdout)
```
PubMed:           found X | queued X | skipped X
Semantic Scholar: found X | queued X | skipped X (or: SKIPPED — no API key)
arXiv:            found X | queued X | skipped X
RSS:              found X | queued X | skipped X
TOTAL queued: X
```

---

## 15. GITHUB ACTIONS SCHEDULE

Repo is PUBLIC — no Actions minute limits.

### Daily ingest (06:00 UTC)
`cron: '0 6 * * *'`
- researcher --source all --days 1
- normalizer
- writer --batch 50
- tagger --batch 50
- verifier

### Weekly deep scan (Sunday 03:00 UTC)
`cron: '0 3 * * 0'`
- researcher --source pubmed --days 7
- normalizer
- writer --batch 100
- tagger --batch 100
- verifier
