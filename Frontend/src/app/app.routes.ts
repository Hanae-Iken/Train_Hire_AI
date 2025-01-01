import { Routes } from '@angular/router';
// import { HomeComponent } from './features/home/home.component'
import { HeroComponent } from './features/home/hero/hero.component';
import { SignupComponent } from './features/auth/signup/signup.component';
import { SigninComponent } from './features/auth/signin/signin.component';
import { AboutComponent } from './features/home/about/about.component';
import { FaqComponent } from './features/home/faq/faq.component';
import { ContactComponent } from './features/home/contact/contact.component';
export const routes: Routes = [
    { path: '', component: HeroComponent },
    { path: 'signup', component: SignupComponent },
    { path: 'signin', component: SigninComponent },
    { path: 'about', component: AboutComponent },
    { path: 'faq', component: FaqComponent },
    { path: 'contact', component: ContactComponent }
    
    

      
];
