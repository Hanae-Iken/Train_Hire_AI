import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterOutlet, NavigationEnd } from '@angular/router';
import { Router } from '@angular/router';
import { filter } from 'rxjs';
@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule,RouterLink],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  isCollapsed: boolean = true; 

  toggleMenu(): void {
    this.isCollapsed = !this.isCollapsed;
  }


  isSignUpOrSignInPage: boolean = false;

  constructor(private router: Router) {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event) => {
      const navigationEvent = event as NavigationEnd;
      this.isSignUpOrSignInPage = navigationEvent.urlAfterRedirects.includes('/signup') || navigationEvent.urlAfterRedirects.includes('/signin');
    });
  }

  ngOnInit() {
    const currentUrl = this.router.url;
    this.isSignUpOrSignInPage = currentUrl.includes('/signup') || currentUrl.includes('/signin');
  }
  

}
