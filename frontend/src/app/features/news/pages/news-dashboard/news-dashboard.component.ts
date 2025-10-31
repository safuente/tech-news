import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { interval, Subscription } from 'rxjs';
import { NewsArticle } from '../../models/news.model';
import { NewsService } from '../../services/news.service';

@Component({
  selector: 'app-news-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './news-dashboard.component.html',
  styleUrls: ['./news-dashboard.component.scss']
})
export class NewsDashboardComponent implements OnInit, OnDestroy {
  articles: NewsArticle[] = [];
  categories: string[] = [
    'technology',
    'business',
    'science',
    'health',
    'sports',
    'entertainment'
  ];
  selectedCategory = 'technology';
  loading = false;
  error: string | null = null;
  fromCache = false;
  private autoRefreshSubscription?: Subscription;

  constructor(private newsService: NewsService) {}

  ngOnInit(): void {
    this.loadNews();
    this.startAutoRefresh();
  }

  ngOnDestroy(): void {
    this.autoRefreshSubscription?.unsubscribe();
  }

  loadNews(): void {
    this.loading = true;
    this.error = null;

    this.newsService.getNews(this.selectedCategory, 1, 6).subscribe({
      next: (response) => {
        this.articles = response.articles;
        this.fromCache = response.from_cache;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Unable to load news. Please try again later.';
        this.loading = false;
        console.error('Error loading news:', err);
      }
    });
  }

  onCategoryChange(category: string): void {
    this.selectedCategory = category;
    this.loadNews();
  }

  startAutoRefresh(): void {
    // Auto refresh every 5 minutes
    this.autoRefreshSubscription = interval(300000).subscribe(() => {
      this.loadNews();
    });
  }

  getCategoryIcon(category: string): string {
    const icons: { [key: string]: string } = {
      technology: '💻',
      business: '💼',
      science: '🔬',
      health: '🏥',
      sports: '⚽',
      entertainment: '🎬'
    };
    return icons[category] || '📰';
  }

  getTimeAgo(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (seconds < 60) return 'just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
  }
}
