import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PreviousmockComponent } from './previousmock.component';

describe('PreviousmockComponent', () => {
  let component: PreviousmockComponent;
  let fixture: ComponentFixture<PreviousmockComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PreviousmockComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PreviousmockComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
