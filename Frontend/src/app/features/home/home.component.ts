import { Component } from '@angular/core';
import { NavbarComponent } from "../../shared/components/navbar/navbar.component";
import { HeroComponent } from "./hero/hero.component";
import { PreloaderComponent } from "../../shared/components/preloader/preloader.component";
import { DomainSearchComponent } from "./domain-search/domain-search.component";
import { BenefitsComponent } from "./benefits/benefits.component";
import { PricingComponent } from "./pricing/pricing.component";
import { AboutComponent } from "./about/about.component";
import { FaqComponent } from "./faq/faq.component";
import { TestimonialComponent } from "./testimonial/testimonial.component";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [NavbarComponent, HeroComponent, PreloaderComponent, DomainSearchComponent, BenefitsComponent, PricingComponent, AboutComponent, FaqComponent, TestimonialComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

}
