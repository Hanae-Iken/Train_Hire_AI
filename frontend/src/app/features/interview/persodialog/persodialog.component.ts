import { Component, EventEmitter, Input, Output , OnInit} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms'; 
import { InterviewService } from '../../../services/interview/interview.service';
import { ResumeService } from '../../../services/resume/resume.service';

@Component({
  selector: 'app-persodialog',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './persodialog.component.html',
  styleUrls: ['./persodialog.component.css']
})
export class PersodialogComponent implements OnInit{
  @Input() isVisible = false;
  @Output() close = new EventEmitter<void>();

  resume: File | null = null;
  title: string = '';
  domain: string = '';
  description: string = '';
  skills: string = '';
  language: string = 'English'; 
  level: string = 'Facile';
  isLoading: boolean = false;
  selectedResume: string = '';
  existingResumes: any[] = [];

  constructor(private interviewService: InterviewService, private router: Router,private resumeService: ResumeService,) {}
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

    // Use the selected resume if available, otherwise use the uploaded file
    if (this.selectedResume) {
      formData.append('selected_resume', this.selectedResume);
    } else if (this.resume) {
      formData.append('uploaded_resume', this.resume);
    }
    console.log('Selected Resume:', this.selectedResume);
    console.log('Uploaded Resume:', this.resume);
    formData.append('title', this.title);
    formData.append('domain', this.domain);
    formData.append('description', this.description);
    formData.append('skills', this.skills);
    formData.append('language', this.language);
    localStorage.setItem('interviewLanguage', this.language);
    console.log('Selected Language:', this.language);
    formData.append('level', this.level);

    for (let [key, value] of (formData as any).entries()) {
      console.log(key, value);
    }
  
    // Start the interview
    this.interviewService.generatePersonalizedInterview(formData).subscribe(
      (response) => {
        console.log('Generated Questions:', response);
  
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
      this.resume = input.files[0];
      console.log('File selected:', this.resume);
    }
  }

  ngOnChanges() {
    console.log("Modal visibility changed:", this.isVisible);
  }

  closeModal() {
    this.close.emit();
  }
}