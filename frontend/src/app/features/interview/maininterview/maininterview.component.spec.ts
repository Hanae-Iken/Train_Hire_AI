import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MaininterviewComponent } from './maininterview.component';

describe('MaininterviewComponent', () => {
  let component: MaininterviewComponent;
  let fixture: ComponentFixture<MaininterviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MaininterviewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MaininterviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
