import { Component } from '@angular/core';
import { NewsDashboardComponent } from './features/news/pages/news-dashboard/news-dashboard.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [NewsDashboardComponent],
  template: '<app-news-dashboard></app-news-dashboard>',
  styles: []
})
export class AppComponent {}
