import httpx
from typing import Optional, Dict, List
from datetime import datetime
import hashlib

from core.config import settings
from core.logger import logger
from core.redis import redis_manager
from schemas.news import NewsArticle, NewsResponse


class NewsService:
    """Service to fetch news from NewsAPI with caching"""
    
    # Available categories
    CATEGORIES = [
        "technology",
        "business",
        "entertainment",
        "health",
        "science",
        "sports",
        "general",
    ]
    
    # Cache metrics
    _cache_hits = 0
    _cache_misses = 0
    
    def __init__(self):
        self.base_url = settings.NEWS_API_BASE_URL
        self.api_key = settings.NEWS_API_KEY
    
    def _get_cache_key(self, category: str, page: int = 1) -> str:
        """Generate unique cache key"""
        return f"news:{category}:page:{page}"
    
    async def get_news(
        self,
        category: str = "technology",
        page: int = 1,
        page_size: int = 5,
        force_refresh: bool = False
    ) -> NewsResponse:
        """
        Get news with caching
        
        Args:
            category: News category
            page: Page number
            page_size: Articles per page
            force_refresh: Force refresh ignoring cache
        """
        # Validate category
        if category not in self.CATEGORIES:
            category = "technology"
        
        cache_key = self._get_cache_key(category, page)
        
        # Try to get from cache
        if not force_refresh:
            cached_data = await redis_manager.get_json(cache_key)
            if cached_data:
                self._cache_hits += 1
                logger.info(f"Cache HIT: {cache_key}")
                
                # Get remaining TTL
                ttl = await redis_manager.get_ttl(cache_key)
                
                return NewsResponse(
                    articles=[NewsArticle(**article) for article in cached_data["articles"]],
                    total_results=cached_data["total_results"],
                    from_cache=True,
                    cache_ttl=ttl if ttl > 0 else None,
                    category=category
                )
        
        # Cache miss - fetch from API
        self._cache_misses += 1
        logger.info(f"Cache MISS: {cache_key}")
        
        # Fetch news from API
        articles_data = await self._fetch_from_api(category, page, page_size)
        
        # Save to cache
        cache_data = {
            "articles": articles_data,
            "total_results": len(articles_data),
        }
        await redis_manager.set_json(
            cache_key,
            cache_data,
            ttl=settings.CACHE_TTL_NEWS
        )
        
        return NewsResponse(
            articles=[NewsArticle(**article) for article in articles_data],
            total_results=len(articles_data),
            from_cache=False,
            cache_ttl=None,
            category=category
        )
    
    async def _fetch_from_api(
        self,
        category: str,
        page: int,
        page_size: int
    ) -> List[Dict]:
        """Fetch news from NewsAPI"""
        
        # If no API key, return mock data
        if not self.api_key:
            logger.warning("NEWS_API_KEY not configured, using mock data")
            return self._get_mock_data(category, page_size)
        
        # Call NewsAPI
        url = f"{self.base_url}/top-headlines"
        params = {
            "category": category,
            "apiKey": self.api_key,
            "page": page,
            "pageSize": page_size,
            "language": "en",
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") != "ok":
                    logger.error(f"NewsAPI error: {data.get('message')}")
                    return self._get_mock_data(category, page_size)
                
                # Transform NewsAPI response to our format
                articles = []
                for item in data.get("articles", [])[:page_size]:
                    articles.append({
                        "id": hashlib.md5(item["url"].encode()).hexdigest(),
                        "title": item.get("title", "No title"),
                        "description": item.get("description"),
                        "content": item.get("content"),
                        "url": item.get("url"),
                        "image_url": item.get("urlToImage"),
                        "published_at": item.get("publishedAt", datetime.now().isoformat()),
                        "source": item.get("source", {}).get("name", "Unknown"),
                        "author": item.get("author"),
                        "category": category,
                    })
                
                logger.info(f"Fetched {len(articles)} articles from NewsAPI")
                return articles
        
        except Exception as e:
            logger.error(f"Error fetching from NewsAPI: {e}")
            return self._get_mock_data(category, page_size)
    
    def _get_mock_data(self, category: str, count: int = 5) -> List[Dict]:
        """Mock data when no API key is available"""
        mock_articles = []
        for i in range(count):
            mock_articles.append({
                "id": f"mock-{category}-{i}",
                "title": f"Example {category.title()} News Article #{i+1}",
                "description": f"This is a mock article about {category} for testing purposes.",
                "content": f"Full content of the {category} article would go here...",
                "url": f"https://example.com/{category}/{i}",
                "image_url": f"https://picsum.photos/800/400?random={i}",
                "published_at": datetime.now().isoformat(),
                "source": "Example News",
                "author": "Test Author",
                "category": category,
            })
        return mock_articles
    
    async def invalidate_cache(self, category: Optional[str] = None) -> int:
        """
        Invalidate cache
        
        Args:
            category: Specific category or None for all
            
        Returns:
            Number of deleted keys
        """
        if category:
            # Invalidate only one category
            pattern = f"news:{category}:*"
        else:
            # Invalidate all news
            pattern = "news:*"
        
        keys = await redis_manager.keys(pattern)
        
        deleted = 0
        for key in keys:
            if await redis_manager.delete(key):
                deleted += 1
        
        logger.info(f"Invalidated {deleted} cache keys (pattern: {pattern})")
        return deleted
    
    def get_metrics(self) -> Dict:
        """Get cache metrics"""
        total = self._cache_hits + self._cache_misses
        hit_rate = (self._cache_hits / total * 100) if total > 0 else 0
        
        return {
            "hits": self._cache_hits,
            "misses": self._cache_misses,
            "total_requests": total,
            "hit_rate_percent": round(hit_rate, 2),
        }
    
    @classmethod
    def get_categories(cls) -> List[str]:
        """Get list of available categories"""
        return cls.CATEGORIES


# Global service instance
news_service = NewsService()
