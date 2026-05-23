// Auto-generated from schema — regenerate with:
// supabase gen types typescript --project-id brxhchmfadzgikoiyflb > apps/web/types/supabase.ts

export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type EnrichmentStatus =
  | 'pending'
  | 'processing'
  | 'auto_committed'
  | 'needs_review'
  | 'rejected'
  | 'flagged'
  | 'failed'

export type SportName =
  | 'running'
  | 'cycling'
  | 'rowing'
  | 'skiing'
  | 'hyrox'
  | 'inline_skating'

export type StudyType =
  | 'RCT'
  | 'cohort'
  | 'review'
  | 'case_study'
  | 'mechanistic'
  | 'meta_analysis'
  | 'cross_sectional'

export type Population =
  | 'recreational'
  | 'trained'
  | 'elite'
  | 'mixed'
  | 'unknown'

export interface Database {
  public: {
    Tables: {
      papers: {
        Row: {
          id: string
          doi: string | null
          title: string
          abstract: string | null
          authors: string[] | null
          journal: string | null
          source_url: string | null
          source_id: string | null
          source_name: string | null
          published_at: string | null
          created_at: string
        }
        Insert: {
          id?: string
          doi?: string | null
          title: string
          abstract?: string | null
          authors?: string[] | null
          journal?: string | null
          source_url?: string | null
          source_id?: string | null
          source_name?: string | null
          published_at?: string | null
          created_at?: string
        }
        Update: {
          id?: string
          doi?: string | null
          title?: string
          abstract?: string | null
          authors?: string[] | null
          journal?: string | null
          source_url?: string | null
          source_id?: string | null
          source_name?: string | null
          published_at?: string | null
          created_at?: string
        }
      }
      enrichments: {
        Row: {
          id: string
          paper_id: string
          summary: string | null
          tags: string[] | null
          sports: string[] | null
          body_regions: string[] | null
          topics: string[] | null
          evidence_level: number | null
          study_type: StudyType | null
          sample_size: number | null
          population: Population | null
          practical_relevance: boolean
          confidence_sports: number | null
          confidence_regions: number | null
          confidence_topics: number | null
          confidence_evidence: number | null
          enrichment_status: EnrichmentStatus
          created_at: string
        }
        Insert: {
          id?: string
          paper_id: string
          summary?: string | null
          tags?: string[] | null
          sports?: string[] | null
          body_regions?: string[] | null
          topics?: string[] | null
          evidence_level?: number | null
          study_type?: StudyType | null
          sample_size?: number | null
          population?: Population | null
          practical_relevance?: boolean
          confidence_sports?: number | null
          confidence_regions?: number | null
          confidence_topics?: number | null
          confidence_evidence?: number | null
          enrichment_status?: EnrichmentStatus
          created_at?: string
        }
        Update: {
          id?: string
          paper_id?: string
          summary?: string | null
          tags?: string[] | null
          sports?: string[] | null
          body_regions?: string[] | null
          topics?: string[] | null
          evidence_level?: number | null
          study_type?: StudyType | null
          sample_size?: number | null
          population?: Population | null
          practical_relevance?: boolean
          confidence_sports?: number | null
          confidence_regions?: number | null
          confidence_topics?: number | null
          confidence_evidence?: number | null
          enrichment_status?: EnrichmentStatus
          created_at?: string
        }
      }
      users: {
        Row: {
          id: string
          email: string | null
          primary_sport: SportName | null
          sport_subcategory: string | null
          preferred_distances: string[] | null
          interests: string[] | null
          onboarded_at: string | null
        }
        Insert: {
          id: string
          email?: string | null
          primary_sport?: SportName | null
          sport_subcategory?: string | null
          preferred_distances?: string[] | null
          interests?: string[] | null
          onboarded_at?: string | null
        }
        Update: {
          id?: string
          email?: string | null
          primary_sport?: SportName | null
          sport_subcategory?: string | null
          preferred_distances?: string[] | null
          interests?: string[] | null
          onboarded_at?: string | null
        }
      }
      saves: {
        Row: {
          id: string
          user_id: string
          paper_id: string
          list_name: string
          saved_at: string
        }
        Insert: {
          id?: string
          user_id: string
          paper_id: string
          list_name?: string
          saved_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          paper_id?: string
          list_name?: string
          saved_at?: string
        }
      }
      ingestion_queue: {
        Row: {
          id: string
          raw: Json
          source: string | null
          status: string
          error: string | null
          created_at: string
        }
        Insert: {
          id?: string
          raw: Json
          source?: string | null
          status?: string
          error?: string | null
          created_at?: string
        }
        Update: {
          id?: string
          raw?: Json
          source?: string | null
          status?: string
          error?: string | null
          created_at?: string
        }
      }
    }
    Views: Record<string, never>
    Functions: Record<string, never>
    Enums: {
      enrichment_status: EnrichmentStatus
      sport_name: SportName
      study_type: StudyType
      population: Population
    }
  }
}

// Convenience type aliases
export type Paper = Database['public']['Tables']['papers']['Row']
export type PaperInsert = Database['public']['Tables']['papers']['Insert']
export type Enrichment = Database['public']['Tables']['enrichments']['Row']
export type EnrichmentInsert = Database['public']['Tables']['enrichments']['Insert']
export type User = Database['public']['Tables']['users']['Row']
export type UserInsert = Database['public']['Tables']['users']['Insert']
export type Save = Database['public']['Tables']['saves']['Row']
export type IngestionQueueItem = Database['public']['Tables']['ingestion_queue']['Row']
