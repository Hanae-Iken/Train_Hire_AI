import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router,RouterLink, RouterOutlet } from '@angular/router';
import { AuthService } from '../../../services/Auth/auth.service';
import { Routes } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [ReactiveFormsModule , RouterLink,CommonModule],  
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css'],
  encapsulation: ViewEncapsulation.ShadowDom,
})
export class SignupComponent implements OnInit {
  signupForm: FormGroup = this.fb.group({
    nom: ['', [Validators.required]],
    prenom: ['', [Validators.required]],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]],
  });
  errorMessage: string = '';
  isLoggedIn: boolean = false; // Track login status
  showLogoutMessage: boolean = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.isLoggedIn = this.authService.isLoggedIn();
  }

  onSubmit(): void {
    if (this.isLoggedIn) {
      this.showLogoutMessage = true;
      return;
    }
    this.signupForm.markAllAsTouched();
    console.log('Form validity:', this.signupForm.valid);
    if (this.signupForm.invalid) {
      console.log('Form is invalid');
      return;
    }

    const formData = this.signupForm.value;
    this.authService.signup(formData).subscribe(
      (response) => {
        console.log('User signed up successfully:', response);
        this.router.navigate(['/signin']); 
      },
      (error) => {
        this.errorMessage = 'Sign-up failed. Please try again later.';
        console.error('Error during sign-up:', error);
      }
    );
  }
}
