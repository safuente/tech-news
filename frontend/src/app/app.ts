
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { NewsService } from './features/news/services/news.service';
import { NewsArticle } from './features/news/models/news.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  providers: [NewsService],
  template: `
    <div class="container">
      <h1>🚀 News Dashboard</h1>

      <div class="controls">
        <button (click)="loadNews()" [disabled]="loading">
          {{ loading ? '⏳ Loading...' : '🔄 Load News' }}
        </button>

        <button (click)="refreshCache()">
          🗑️ Clear Cache
        </button>
      </div>

      <div *ngIf="error" class="error">
        ❌ {{ error }}
      </div>

      <div *ngIf="loading" class="loading">
        Loading news...
      </div>

      <div *ngIf="!loading && articles.length > 0" class="news-grid">
        <div *ngFor="let article of articles" class="news-card">
          <img [src]="article.image_url || 'https://via.placeholder.com/400x200'"
               [alt]="article.title">
          <div class="content">
            <span class="source">{{ article.source }}</span>
            <h3>{{ article.title }}</h3>
            <p>{{ article.description }}</p>
            <a [href]="article.url" target="_blank">Read more →</a>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }

    h1 {
      text-align: center;
      color: #3498db;
    }

    .controls {
      display: flex;
      gap: 10px;
      justify-content: center;
      margin: 20px 0;
    }

    button {
      padding: 12px 24px;
      font-size: 1rem;
      background: #3498db;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
    }

    button:hover {
      background: #2980b9;
    }

    button:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    .error {
      padding: 15px;
      background: #fee;
      border-left: 4px solid #e74c3c;
      border-radius: 4px;
      margin: 20px 0;
      color: #c0392b;
    }

    .loading {
      text-align: center;
      padding: 40px;
      color: #7f8c8d;
    }

    .news-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 24px;
      margin-top: 30px;
    }

    .news-card {
      background: white;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      transition: transform 0.3s;
    }

    .news-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }

    .news-card img {
      width: 100%;
      height: 200px;
      object-fit: cover;
    }

    .content {
      padding: 20px;
    }

    .source {
      color: #3498db;
      font-size: 0.85rem;
      font-weight: 600;
      text-transform: uppercase;
    }

    h3 {
      margin: 10px 0;
      color: #2c3e50;
    }

    p {
      color: #7f8c8d;
      line-height: 1.6;
    }

    a {
      display: inline-block;
      margin-top: 10px;
      color: #3498db;
      text-decoration: none;
      font-weight: 600;
    }

    a:hover {
      text-decoration: underline;
    }
  `]
})
export class AppComponent implements OnInit {
  articles: NewsArticle[] = [];
  loading = false;
  error: string | null = null;

  constructor(private newsService: NewsService) {}

  ngOnInit() {
    this.loadNews();
  }

  loadNews() {
    this.loading = true;
    this.error = null;

    this.newsService.getNews('technology', 1, 6).subscribe({
      next: (response) => {
        this.articles = response.articles;
        this.loading = false;
        console.log('News loaded:', response);
      },
      error: (err) => {
        this.error = 'Error loading news';
        this.loading = false;
        console.error('Error:', err);
      }
    });
  }

  refreshCache() {
    this.newsService.refreshCache().subscribe({
      next: () => {
        console.log('Cache cleared');
        this.loadNews();
      },
      error: (err) => {
        console.error('Error clearing cache:', err);
      }
    });
  }
}
