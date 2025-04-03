import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PersodialogComponent } from './persodialog.component';

describe('PersodialogComponent', () => {
  let component: PersodialogComponent;
  let fixture: ComponentFixture<PersodialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PersodialogComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PersodialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
