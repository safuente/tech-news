import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { NewsResponse, CacheMetrics } from '../models/news.model';

@Injectable({
  providedIn: 'root'
})
export class NewsService {
  private apiUrl = 'http://localhost:9000/api/news';

  constructor(private http: HttpClient) {}

  /**
   * Get news articles
   */
  getNews(
    category: string = 'technology',
    page: number = 1,
    pageSize: number = 6,
    forceRefresh: boolean = false
  ): Observable<NewsResponse> {
    const params = new HttpParams()
      .set('category', category)
      .set('page', page.toString())
      .set('page_size', pageSize.toString())
      .set('force_refresh', forceRefresh.toString());

    return this.http.get<NewsResponse>(`${this.apiUrl}/`, { params });
  }

  /**
   * Get available categories
   */
  getCategories(): Observable<{ categories: string[] }> {
    return this.http.get<{ categories: string[] }>(`${this.apiUrl}/categories`);
  }

  /**
   * Get cache metrics
   */
  getCacheMetrics(): Observable<CacheMetrics> {
    return this.http.get<CacheMetrics>(`${this.apiUrl}/metrics`);
  }

  /**
   * Refresh cache
   */
  refreshCache(category?: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/refresh`, {
      category: category || null,
      invalidate_all: !category
    });
  }
}
