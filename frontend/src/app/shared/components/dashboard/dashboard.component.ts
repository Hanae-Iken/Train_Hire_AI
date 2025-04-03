import { Component, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule,Router } from '@angular/router';
import { GeninterviewComponent } from '../../../features/interview/geninterview/geninterview.component';
// import { AuthService } from '../../../services/Auth/auth.service';
import { WelcomeComponent } from '../../../features/interview/welcome/welcome.component';

import { AuthService } from '../../../services/Auth/auth.service';
import { ResumeComponent } from '../../../features/interview/resume/resume.component';
import { PreviousmockComponent } from '../../../features/interview/previousmock/previousmock.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, GeninterviewComponent,WelcomeComponent],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  encapsulation: ViewEncapsulation.ShadowDom,
})

export class DashboardComponent {
  isSidebarHidden: boolean = false; // Sidebar visibility toggle
  selectedContent: string = 'welcome';
  welcomeMessage: string = '';
  searchQuery: string = '';
  sideMenuItems: any[] = [
    { name: 'Tableau de bord', icon: 'bx bxs-dashboard', active: true, route: '/dashboard/welcome' },
    { name: 'Mock Interview', icon: 'bx bxs-shopping-bag-alt', active: false, route: '/dashboard/gen-interview' },
    { name: 'Previous Mocks', icon: 'bx bxs-doughnut-chart', active: false, route : '/dashboard/previousmock'},
    { name: 'Upload CV', icon: 'bx bxs-message-dots', active: false, route : '/dashboard/resume' },
  ];
  

  constructor(private authService: AuthService, private router: Router) {}

  // ngOnInit(): void {
  //   const user = this.authService.getUser();
  //   this.welcomeMessage = user && user.prenom && user.nom
  //     ? `Hello ${user.prenom} ${user.nom}!`
  //     : 'Hello!';
  // }
  logout() {
    this.authService.logout().subscribe(() => {
      // Redirect to the login page after logout
      this.router.navigate(['/signin']);
    });
  }

  toggleSidebar(): void {
    this.isSidebarHidden = !this.isSidebarHidden;
  }

  selectMenu(item: any): void {
    this.sideMenuItems.forEach(i => i.active = false);
    item.active = true;
    this.selectedContent = item.name;

    // Check if the selected content is "Gen Interview"
    if (item.name === 'Mock Interview') {
      this.selectedContent = 'gen-interview'; // Set to the identifier for the component
    }
    if (item.name === 'Tableau de bord') {
      this.selectedContent = 'welcome'; // Set to the identifier for the component
    }
    if (item.name === 'resume') {
      this.selectedContent = 'resume'; // Set to the identifier for the component
    }
  }

  toggleDarkMode(event: any): void {
    const rootElement = document.querySelector('all'); // Target the content section or other parent
    if (event.target.checked) {
      rootElement?.classList.add('dark');
    } else {
      rootElement?.classList.remove('dark');
    }
  }
  

  onSearch(event: Event): void {
    event.preventDefault();
    console.log('Searching for:', this.searchQuery);
  }
}
