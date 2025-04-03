import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GeninterviewComponent } from './geninterview.component';

describe('GeninterviewComponent', () => {
  let component: GeninterviewComponent;
  let fixture: ComponentFixture<GeninterviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GeninterviewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GeninterviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
