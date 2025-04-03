import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-results',
  standalone: true, // Mark as standalone
  imports: [CommonModule],
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {
  feedbackResults: any[] = [];

  constructor(private router: Router) {
    // Retrieve the feedback results from the state
    const navigation = this.router.getCurrentNavigation();
    if (navigation?.extras.state) {
      this.feedbackResults = navigation.extras.state['feedbackResults'];
    }
  }

  ngOnInit(): void {
    if (!this.feedbackResults || this.feedbackResults.length === 0) {
      console.error('No feedback results found. Redirecting to home.');
      this.router.navigate(['/']);
    }
  }
}