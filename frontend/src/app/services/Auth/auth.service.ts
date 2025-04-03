import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/'; // Your Django API URL

  constructor(private http: HttpClient, private cookieService: CookieService) { }

  // getCsrfToken(): string {
  //   return this.cookieService.get('csrftoken') || '';
  // }

  // getHeaders(): HttpHeaders {
  //   const headers = new HttpHeaders({
  //     'X-CSRFToken': this.getCsrfToken(),
  //     'Content-Type': 'application/json',
  //   });
  //   return headers;
  // }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('sessionId'); // Check if sessionId exists
  }

  signup(userData: any): Observable<any> {
    
    return this.http.post(`${this.apiUrl}signup/`, userData, {  withCredentials: true });
  }

  signin(userData: any): Observable<any> {
    const csrfToken = this.cookieService.get('csrftoken'); // Get CSRF token from cookies
    console.log('CSRF Token:', csrfToken);
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken, // Send CSRF token
      'Content-Type': 'application/json',
    });
  
    return this.http.post(`${this.apiUrl}signin/`, userData, { 
      headers: headers,
      withCredentials: true 
    }).pipe(
      tap((response: any) => {
        localStorage.setItem('sessionId', response.sessionId);
        localStorage.setItem('csrftoken', csrfToken);
        localStorage.setItem('user', JSON.stringify(response.user));
      })
    );
  }
  

  // logout(): Observable<any> {
  //   return this.http.post(`${this.apiUrl}logout/`, {}, { withCredentials: true }).pipe(
  //     tap(() => {
  //       // Clear the sessionId, csrftoken, and user data from localStorage
  //       localStorage.removeItem('sessionId');
  //       localStorage.removeItem('csrftoken');
  //       localStorage.removeItem('user');
  //       this.cookieService.delete('csrftoken');
  //     })
  //   );
  // }

  logout(): Observable<any> {
    const csrfToken = this.cookieService.get('csrftoken'); // Get CSRF token from cookies
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken, // Include CSRF token in headers
      'Content-Type': 'application/json',
    });
  
    return this.http.post(`${this.apiUrl}logout/`, {}, { headers, withCredentials: true }).pipe(
      tap(() => {
        // Clear the sessionId, csrftoken, and user data from localStorage
        localStorage.removeItem('sessionId');
        localStorage.removeItem('csrftoken');
        localStorage.removeItem('user');
  
        // Clear the CSRF token cookie
        this.cookieService.delete('csrftoken','/');
      })
    );
  }

  
  setUser(user: any) {
    localStorage.setItem('user', JSON.stringify(user));
  }

  getUser() {
    return JSON.parse(localStorage.getItem('user') || '{}');
  }

  clearUser() {
    localStorage.removeItem('user');
  }

  

  getSessionId(): string {
    return localStorage.getItem('sessionId') || '';
  }
}