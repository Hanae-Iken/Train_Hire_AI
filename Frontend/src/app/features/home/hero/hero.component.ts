import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AnimationOptions,LottieComponent } from 'ngx-lottie';
import { AnimationItem } from 'lottie-web';
@Component({
  selector: 'app-hero',
  standalone: true,
  imports: [RouterLink,LottieComponent],
  templateUrl: './hero.component.html',
  styleUrl: './hero.component.css',
})
export class HeroComponent {
  options: AnimationOptions = {
    path: '/assets/Homepage/img/hero/robotAnimation.json', 
  };
}
