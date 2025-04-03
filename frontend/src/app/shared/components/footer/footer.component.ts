import { Component,OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { filter } from 'rxjs';
import {  NavigationEnd } from '@angular/router';
import { CommonModule } from '@angular/common';
import { RouterLink} from '@angular/router';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.css'
})
export class FooterComponent {
   isSignUpOrSignInPage: boolean = false;
  
    constructor(private router: Router) {
      this.router.events.pipe(
        filter(event => event instanceof NavigationEnd)
      ).subscribe((event) => {
        const navigationEvent = event as NavigationEnd;
        this.isSignUpOrSignInPage = navigationEvent.urlAfterRedirects.includes('/signup') || navigationEvent.urlAfterRedirects.includes('/signin') || navigationEvent.urlAfterRedirects.includes('/dashboard');
      });
    }
  
    ngOnInit() {
      const currentUrl = this.router.url;
      this.isSignUpOrSignInPage = currentUrl.includes('/signup') || currentUrl.includes('/signin')|| currentUrl.includes('/dashboard');
    }

}
