import { Component, ViewEncapsulation, OnInit } from '@angular/core';
import { ResumeService } from '../../../services/resume/resume.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-resume',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './resume.component.html',
  styleUrl: './resume.component.css',
  encapsulation: ViewEncapsulation.ShadowDom
})
export class ResumeComponent implements OnInit {
  resumes: any[] = [];
  selectedFile: File | null = null;

  constructor(private resumeService: ResumeService) {}

  ngOnInit(): void {
    this.listResumes();
  }

  // Method to list all resumes
  listResumes(): void {
    this.resumeService.listResumes().subscribe(
      (data: any) => {
        this.resumes = data.resumes;
      },
      (error) => {
        console.error('Error fetching resumes', error);
      }
    );
  }

  // Method to handle file change (for uploading resume)
  onFileChange(event: any): void {
    this.selectedFile = event.target.files[0];
    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('resume', this.selectedFile);
      this.uploadResume(formData);
    }
  }

  // Method to upload resume
  uploadResume(formData: FormData): void {
    this.resumeService.uploadResume(formData).subscribe(
      (response) => {
        console.log('Resume uploaded successfully', response);
        this.listResumes();  // Refresh the list of resumes
      },
      (error) => {
        console.error('Error uploading resume', error);
      }
    );
  }

  // Method to delete a resume
  deleteResume(resumeId: number): void {
    this.resumeService.deleteResume(resumeId).subscribe(
      (response) => {
        console.log('Resume deleted successfully', response);
        this.listResumes();  // Refresh the list of resumes
      },
      (error) => {
        console.error('Error deleting resume', error);
      }
    );
  }

  // Method to view a resume (trigger download or open in a new window)
  viewResume(resumeId: number): void {
    this.resumeService.viewResume(resumeId).subscribe(
      (response: any) => {
        // This might trigger a file download
        const blob = new Blob([response], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
        window.open(url, '_blank');
      },
      (error) => {
        console.error('Error viewing resume', error);
      }
    );
  }

  

}
