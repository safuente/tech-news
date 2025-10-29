export interface NewsArticle {
  id: string;
  title: string;
  description: string | null;
  content: string | null;
  url: string;
  image_url: string | null;
  published_at: string;
  source: string;
  author: string | null;
  category: string;
}

export interface NewsResponse {
  articles: NewsArticle[];
  total_results: number;
  from_cache: boolean;
  cache_ttl: number | null;
  category: string;
}

export interface CacheMetrics {
  hits: number;
  misses: number;
  total_requests: number;
  hit_rate_percent: number;
}
