from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from schemas.news import (
    NewsResponse,
    CacheRefreshRequest,
    CacheRefreshResponse,
    CacheMetrics,
)
from services.news_service import news_service
from core.logger import logger

router = APIRouter()


@router.get("/", response_model=NewsResponse)
async def get_news(
    category: str = Query("technology", description="News category"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(5, ge=1, le=20, description="Articles per page"),
    force_refresh: bool = Query(False, description="Force cache refresh"),
):
    """
    Get news with Redis caching
    
    - **category**: News category (technology, business, sports, etc.)
    - **page**: Page number
    - **page_size**: Number of articles per page (max 20)
    - **force_refresh**: true to ignore cache and get fresh data
    """
    try:
        logger.info(f"GET /api/news/ - category={category}, page={page}, force_refresh={force_refresh}")
        news_response = await news_service.get_news(
            category=category,
            page=page,
            page_size=page_size,
            force_refresh=force_refresh
        )
        return news_response
    except Exception as e:
        logger.error(f"Error getting news: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories", response_model=dict)
async def get_categories():
    """
    Get list of available news categories
    """
    return {
        "categories": news_service.get_categories()
    }


@router.post("/refresh", response_model=CacheRefreshResponse)
async def refresh_cache(request: CacheRefreshRequest):
    """
    Invalidate cache
    
    - **category**: Specific category to invalidate (null = all)
    - **invalidate_all**: true to invalidate all cache
    """
    try:
        category = None if request.invalidate_all else request.category
        
        deleted_count = await news_service.invalidate_cache(category)
        
        if category:
            message = f"Category '{category}' cache invalidated"
        else:
            message = "All news cache invalidated"
        
        logger.info(f"Cache refresh: {message} ({deleted_count} keys deleted)")
        
        return CacheRefreshResponse(
            message=message,
            keys_deleted=deleted_count
        )
    except Exception as e:
        logger.error(f"Error refreshing cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics", response_model=CacheMetrics)
async def get_cache_metrics():
    """
    Get cache performance metrics
    
    Returns statistics about cache hits, misses, and hit rate
    """
    metrics = news_service.get_metrics()
    return CacheMetrics(**metrics)
