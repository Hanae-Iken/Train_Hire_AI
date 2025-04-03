import { Routes } from '@angular/router';
// import { HomeComponent } from './features/home/home.component'
import { HeroComponent } from './features/home/hero/hero.component';
import { SignupComponent } from './features/auth/signup/signup.component';
import { SigninComponent } from './features/auth/signin/signin.component';
import { AboutComponent } from './features/home/about/about.component';
import { FaqComponent } from './features/home/faq/faq.component';
import { ContactComponent } from './features/home/contact/contact.component';
import { DashboardComponent } from './shared/components/dashboard/dashboard.component';
import { GeninterviewComponent } from './features/interview/geninterview/geninterview.component';
import { WelcomeComponent } from './features/interview/welcome/welcome.component';
import { MainInterviewComponent } from './features/interview/maininterview/maininterview.component';
import { authGuard } from './guards/auth.guard';
import { ResultsComponent } from './features/interview/results/results.component';
import { ResumeComponent } from './features/interview/resume/resume.component';
import { PreviousmockComponent } from './features/interview/previousmock/previousmock.component';
import { PreviousfeedComponent } from './features/interview/previousfeed/previousfeed.component';

export const routes: Routes = [
    { path: '', component: HeroComponent },
    { path: 'signup', component: SignupComponent },
    { path: 'signin', component: SigninComponent },
    { path: 'about', component: AboutComponent },
    { path: 'faq', component: FaqComponent },
    { path: 'contact', component: ContactComponent },
    { path: 'dashboard' , component: DashboardComponent ,canActivate: [authGuard],
        children: [
            { path: 'welcome', component: WelcomeComponent},
            { path: 'gen-interview', component: GeninterviewComponent},
            { path: 'main-interview' , component: MainInterviewComponent},
            { path: 'result' , component: ResultsComponent},
            { path: 'resume' , component: ResumeComponent},
            { path: 'previousmock' , component: PreviousmockComponent},
            { path: 'previousfeed/:sessionId', component: PreviousfeedComponent },
            { path: '', redirectTo: 'welcome', pathMatch: 'full' },  // Default route
            { path: '**', redirectTo: 'welcome' } // Fallback for unknown routes
        ]
    } ,
    // { path: 'gen-interview' , component: GeninterviewComponent} ,
    // { path: 'welcome' , component: GeninterviewComponent,canActivate: [authGuard]} ,
    // { path: 'main-interview' , component: MaininterviewComponent,canActivate:[authGuard]},
    { path: '**', redirectTo: 'signin' }


       

];
