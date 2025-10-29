from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime


class NewsArticle(BaseModel):
    """News article model"""
    id: str = Field(..., description="Unique article ID")
    title: str = Field(..., description="Article title")
    description: Optional[str] = Field(None, description="Short description")
    content: Optional[str] = Field(None, description="Full content")
    url: HttpUrl = Field(..., description="Original article URL")
    image_url: Optional[HttpUrl] = Field(None, description="Image URL")
    published_at: datetime = Field(..., description="Publication date")
    source: str = Field(..., description="News source")
    author: Optional[str] = Field(None, description="Article author")
    category: str = Field(..., description="News category")


class NewsResponse(BaseModel):
    """News list response"""
    articles: List[NewsArticle] = Field(..., description="List of articles")
    total_results: int = Field(..., description="Total results")
    from_cache: bool = Field(..., description="Whether data came from cache")
    cache_ttl: Optional[int] = Field(None, description="Remaining cache TTL (seconds)")
    category: str = Field(..., description="Queried category")


class CacheRefreshRequest(BaseModel):
    """Cache invalidation request"""
    category: Optional[str] = Field(None, description="Category to invalidate (None = all)")
    invalidate_all: bool = Field(False, description="Invalidate all cache")


class CacheRefreshResponse(BaseModel):
    """Cache invalidation response"""
    message: str
    keys_deleted: int


class CacheMetrics(BaseModel):
    """Cache metrics"""
    hits: int = Field(..., description="Number of cache hits")
    misses: int = Field(..., description="Number of cache misses")
    total_requests: int = Field(..., description="Total requests")
    hit_rate_percent: float = Field(..., description="Hit rate percentage")
