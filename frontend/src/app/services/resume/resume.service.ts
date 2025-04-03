import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from '../Auth/auth.service';
import { CookieService } from 'ngx-cookie-service';



@Injectable({
  providedIn: 'root'
})
export class ResumeService {
  private apiUrl = 'http://localhost:8000/resumes';

  constructor(private http: HttpClient,private authService: AuthService,private cookieService: CookieService, ) { }

  // Method to upload a resume
  uploadResume(formData: FormData): Observable<any> {
    return this.http.post(`${this.apiUrl}/upload/`, formData, {
      withCredentials: true,
    });
  }

  // Method to delete a resume
  deleteResume(resumeId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/delete/${resumeId}/`, {}, {
      withCredentials: true,
    });
  }

  // Method to list all resumes
  listResumes(): Observable<any> {
    return this.http.get(`${this.apiUrl}/list/`, {
      withCredentials: true,
    });
  }

  // Method to view a resume
  viewResume(resumeId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/view/${resumeId}/`, {
      withCredentials: true,
      responseType: 'blob',  // Assuming it's a file, you may need to adjust MIME type handling
    });
  }
}
