import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router,RouterLink } from '@angular/router';
import { AuthService } from '../../../services/Auth/auth.service';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-signin',
  standalone: true,
  imports: [ReactiveFormsModule , CommonModule ,RouterLink,], 
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css'],
  encapsulation: ViewEncapsulation.ShadowDom,
})
export class SigninComponent implements OnInit {
  signinForm: FormGroup;
  errorMessage: string = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.signinForm = this.fb.group({
      email: ['', [Validators.required]],
      password: ['', [Validators.required]],
    });
  }

  ngOnInit(): void {}

  onSubmit(): void {
    if (this.signinForm.invalid) {
      console.log('Form is invalid');
      return;
    }

    const formData = this.signinForm.value;
    console.log('Form Data:', formData);
    this.authService.signin(formData).subscribe(
      (response) => {
        console.log('User signed in successfully:', response);
        this.authService.setUser(response.user); // Save user data
        this.router.navigate(['/dashboard']); // Redirect to home or dashboard
      },
      (error) => {
        this.errorMessage = 'Sign-in failed. Please check your credentials.';
        console.error('Error during sign-in:', error);
      }
    );
  }
}