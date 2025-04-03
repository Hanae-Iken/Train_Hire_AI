import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GendialogComponent } from './gendialog.component';

describe('GendialogComponent', () => {
  let component: GendialogComponent;
  let fixture: ComponentFixture<GendialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GendialogComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GendialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
