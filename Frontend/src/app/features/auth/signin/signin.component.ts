import { Component, ViewEncapsulation } from '@angular/core';
import { RouterLink } from '@angular/router';
@Component({
  selector: 'app-signin',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './signin.component.html',
  styleUrl: './signin.component.css',
  encapsulation: ViewEncapsulation.ShadowDom,
})
export class SigninComponent {

}
