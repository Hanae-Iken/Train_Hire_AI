import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { RouterLink, RouterOutlet } from '@angular/router';
import { HomeComponent } from "./features/home/home.component";
import { PreloaderComponent } from './shared/components/preloader/preloader.component';
import { NavbarComponent } from "./shared/components/navbar/navbar.component";
import { HeroComponent } from "./features/home/hero/hero.component";
import { AboutComponent } from "./features/home/about/about.component";
import { FooterComponent } from "./shared/components/footer/footer.component";
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [HomeComponent, RouterOutlet, NavbarComponent, PreloaderComponent, FooterComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Angular7';

}

