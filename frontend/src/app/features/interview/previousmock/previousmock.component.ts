import { Component, OnInit } from '@angular/core';
import { InterviewService } from '../../../services/interview/interview.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-previousmock',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './previousmock.component.html',
  styleUrl: './previousmock.component.css'
})
export class PreviousmockComponent implements OnInit{
  previousInterviews: any[] = []; 

  constructor(private interviewService: InterviewService, private router: Router) {}

  ngOnInit(): void {
    this.loadPreviousInterviews();
  }

  loadPreviousInterviews(): void {
    this.interviewService.getPreviousInterviews().subscribe(
      (data: any) => {
        this.previousInterviews = data.sessions; // Assuming the API returns an object with a 'sessions' array
      },
      (error) => {
        console.error('Error fetching previous interviews:', error);
      }
    );
  }

  navigateToFeedback(sessionId: string): void {
    this.router.navigate(['/dashboard/previousfeed', sessionId]);
  }

}
