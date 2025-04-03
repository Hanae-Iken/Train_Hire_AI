import { Component } from '@angular/core';
import { AuthService } from '../../../services/Auth/auth.service';
@Component({
  selector: 'app-welcome',
  standalone: true,
  imports: [],
  templateUrl: './welcome.component.html',
  styleUrl: './welcome.component.css'
})
export class WelcomeComponent {
  welcomeMessage: string = '';
  constructor(private authService: AuthService) {}
  ngOnInit(): void {
    const user = this.authService.getUser();
    this.welcomeMessage = user && user.prenom && user.nom
      ? `Hello ${user.prenom} ${user.nom}!`
      : 'Hello!';
  }

}
