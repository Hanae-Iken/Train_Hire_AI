// modal.service.ts
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ModalService {
  private modalVisibility = new BehaviorSubject<boolean>(false);
  modalState$ = this.modalVisibility.asObservable();

  openModal() {
    this.modalVisibility.next(true);
  }

  closeModal() {
    this.modalVisibility.next(false);
  }
}