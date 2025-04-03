import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';
import { AuthService } from '../Auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class InterviewService {
  private apiUrlPersonalized = 'http://localhost:8000/gen_personalized_interview/'; // Django URL for personalized interviews
  private apiUrlGeneral = 'http://localhost:8000/gen_general_interview/'; // Django URL for general interviews
  private apiQstForSession = 'http://localhost:8000/get_questions_for_session/'; // Updated URL for fetching questions
  private apiHandleResponse = 'http://localhost:8000/handle_audio_response/'; // Updated URL for handling responses
  private apiAnalyzeInterview = 'http://localhost:8000/analyze_interview/';
  private apiPreviousInterviews = 'http://localhost:8000/get_previous_interviews/';
  private apiFeedbackDetails = 'http://localhost:8000/get_feedback_details/';

  constructor(
    private http: HttpClient,
    private cookieService: CookieService,
    private authService: AuthService
  ) {}

  // Method to start an interview
  startInterview(): Observable<any> {
    return this.http.post('http://localhost:8000/start_interview/', {}, {
      withCredentials: true,
    });
  }

  // Method to generate personalized interview questions
  generatePersonalizedInterview(data: any): Observable<any> {
    return this.http.post(this.apiUrlPersonalized, data, {
      withCredentials: true,
    });
  }

  // Method to generate generalized interview questions
  generateGeneralInterview(data: any): Observable<any> {
    return this.http.post(this.apiUrlGeneral, data, {
      withCredentials: true,
    });
  }

  // Method to fetch questions for a session
  getQuestionsForSession(sessionId: string): Observable<any> {
    return this.http.get(`${this.apiQstForSession}${sessionId}/`, {
      withCredentials: true, // Add withCredentials here
    });
  }

  // Method to upload audio response
  uploadResponse(formData: FormData): Observable<any> {
    return this.http.post(this.apiHandleResponse, formData, {
      withCredentials: true,
    });
  }

  analyzeInterview(): Observable<any> {
    return this.http.post(this.apiAnalyzeInterview, {}, {
      withCredentials: true,
    });
  }

  getPreviousInterviews(): Observable<any> {
    return this.http.get(this.apiPreviousInterviews, {
      withCredentials: true,
    });
  }

  getFeedbackDetails(sessionId: number): Observable<any> {
    return this.http.get(`${this.apiFeedbackDetails}${sessionId}/`, {
      withCredentials: true,
    });
  }
}