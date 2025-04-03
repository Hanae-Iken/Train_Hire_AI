import { Component , ViewEncapsulation} from '@angular/core';
import { AuthService } from '../../../services/Auth/auth.service';
import { ModalService } from '../persodialog/perso.service';
import { PersodialogComponent } from "../persodialog/persodialog.component";
import { GendialogComponent } from '../gendialog/gendialog.component';
import { InterviewService } from '../../../services/interview/interview.service';
@Component({
  selector: 'app-geninterview',
  standalone: true,
  imports: [PersodialogComponent,GendialogComponent ],
  templateUrl: './geninterview.component.html',
  styleUrl: './geninterview.component.css',
  encapsulation: ViewEncapsulation.ShadowDom,
})
export class GeninterviewComponent {
  welcomeMessage: string = '';
  showPersoModal = false;
  showGenModal = false;

  constructor(private authService: AuthService , private interviewService: InterviewService) {}

  ngOnInit(): void {
    const user = this.authService.getUser();
    this.welcomeMessage = user && user.prenom && user.nom ? ` ${user.nom}` : '';
  }

  // openPersoModal() {
  //   this.showPersoModal = true;
  //   this.showGenModal = false; // Ensure the other modal is closed
  // }

  openPersoModal() {
    this.interviewService.startInterview().subscribe({
      next: (response) => {
        console.log('Interview session started:', response);
        this.showPersoModal = true;
        this.showGenModal = false; // Ensure the other modal is closed
      },
      error: (error) => {
        console.error('Error starting interview:', error);
      }
    });
  }

  openGenModal() {
    this.showGenModal = true;
    this.showPersoModal = false; 
    this.interviewService.startInterview().subscribe({
      next: (response) => {
        console.log('Interview session started:', response);
        this.showPersoModal = false;
        this.showGenModal = true; // Ensure the other modal is closed
      },
      error: (error) => {
        console.error('Error starting interview:', error);
      }
    });
  }

  closePersoModal() {
    this.showPersoModal = false;
  }

  closeGenModal() {
    this.showGenModal = false;
  }
}

