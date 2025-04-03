import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PreviousfeedComponent } from './previousfeed.component';

describe('PreviousfeedComponent', () => {
  let component: PreviousfeedComponent;
  let fixture: ComponentFixture<PreviousfeedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PreviousfeedComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PreviousfeedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
