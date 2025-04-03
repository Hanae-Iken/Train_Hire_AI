import { Component, EventEmitter, Input, Output , OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { InterviewService } from '../../../services/interview/interview.service';
import { FormsModule } from '@angular/forms'; 
import { ResumeService } from '../../../services/resume/resume.service';



@Component({
  selector: 'app-gendialog',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './gendialog.component.html',
  styleUrl: './gendialog.component.css'
})
export class GendialogComponent implements OnInit{

  @Input() isVisible = false;
  @Output() close = new EventEmitter<void>();
  resume: File | null = null;
  language: string = 'English'; 
  level: string = 'Facile';
  isLoading: boolean = false;
  selectedResume: string = '';
  existingResumes: any[] = [];


   constructor(private interviewService: InterviewService, private router: Router,private resumeService: ResumeService) {}
   ngOnInit(): void {
    this.fetchExistingResumes();
  }
  fetchExistingResumes(): void {
    this.resumeService.listResumes().subscribe(
      (data: any) => {
        this.existingResumes = data.resumes;
      },
      (error) => {
        console.error('Error fetching resumes:', error);
      }
    );
  }
   startInterview() {
    this.isLoading = true;
    const formData = new FormData();
    if (this.selectedResume) {
      formData.append('selected_resume', this.selectedResume);
      console.log('Selected Resume ID:', this.selectedResume);
    } else if (this.resume) {
      formData.append('uploaded_resume', this.resume);
    }
    formData.append('language', this.language);
    formData.append('level', this.level);

    this.interviewService.generateGeneralInterview(formData).subscribe(
      (response) => {
        console.log('Generated Questions:', response);
        // Handle the response (e.g., show questions in modal)
         // Store the session ID in LocalStorage or a service
         localStorage.setItem('interviewSessionId', response.session_id);
         this.isLoading = false;
   
         this.closeModal();
         // Redirect to the main interview page
         console.log('Navigating to /dashboard/main-interview');
         this.router.navigate(['/dashboard/main-interview']);
      },
      (error) => {
        console.error('Error generating questions:', error);
        this.isLoading = false;
      }
    );
   }

   onFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
        this.resume = input.files[0]; // Set the uploaded file
        console.log('Resume file set:', this.resume);
    } else {
        console.log('No file selected');
    }
}

  ngOnChanges() {
    console.log("Modal visibility changed:", this.isVisible);
  }

  closeModal() {
    this.close.emit();
  }

}
