import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { InterviewService } from '../../../services/interview/interview.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-previousfeed',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './previousfeed.component.html',
  styleUrl: './previousfeed.component.css'
})
export class PreviousfeedComponent implements OnInit {
  feedbackDetails: any;

  constructor(private route: ActivatedRoute, private interviewService: InterviewService) {}

  ngOnInit(): void {
    const sessionId = this.route.snapshot.paramMap.get('sessionId');
    if (sessionId) {
      this.loadFeedbackDetails(sessionId);
    }
  }

  loadFeedbackDetails(sessionId: string): void {
    const sessionIdNumber = Number(sessionId); // Convert string to number
    if (isNaN(sessionIdNumber)) {
      console.error('Invalid session ID:', sessionId);
      return;
    }
  
    this.interviewService.getFeedbackDetails(sessionIdNumber).subscribe(
      (data: any) => {
        this.feedbackDetails = data;
      },
      (error) => {
        console.error('Error fetching feedback details:', error);
      }
    );
  }

}
