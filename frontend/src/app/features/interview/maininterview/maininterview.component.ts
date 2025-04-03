import { Component, OnInit, ChangeDetectorRef, ViewChild, ElementRef } from '@angular/core';
import { InterviewService } from '../../../services/interview/interview.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { DomSanitizer } from '@angular/platform-browser';
import * as RecordRTC from 'recordrtc';
import { PreloaderComponent } from "../../../shared/components/preloader/preloader.component";

@Component({
  selector: 'app-main-interview',
  standalone: true,
  imports: [CommonModule, PreloaderComponent],
  templateUrl: './maininterview.component.html',
  styleUrls: ['./maininterview.component.css']
})
export class MainInterviewComponent implements OnInit {
  sessionId: string | null = null;
  questions: any[] = [];
  currentQuestionIndex: number = 0;
  isAudioPlaying = false;
  @ViewChild('videoElement') videoRef!: ElementRef;
  @ViewChild('audioElement') audioElement!: ElementRef<HTMLAudioElement>;

  record: any;
  recording = false;
  url: any;
  error: any;
  isLoading: boolean = false;
  analysisMessage: string = '';

  constructor(
    private interviewService: InterviewService,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private domSanitize: DomSanitizer
  ) {}

  ngOnInit(): void {
    this.sessionId = localStorage.getItem('interviewSessionId');
    this.setupCamera();

    if (this.sessionId) {
      this.fetchQuestions();
    } else {
      console.error('No session ID found. Redirecting to home.');
      this.router.navigate(['/']);
    }
  }

  fetchQuestions() {
    if (this.sessionId) {
      this.interviewService.getQuestionsForSession(this.sessionId).subscribe(
        (response: any) => {
          this.questions = response.questions.map((question: any) => ({
            ...question,
            audio_url: `http://localhost:8000${question.audio_url}`
          }));
          this.cdr.detectChanges();
          this.playAudio();
        },
        (error) => {
          console.error('Error fetching questions:', error);
        }
      );
    }
  }



  async nextQuestion() {
    if (this.currentQuestionIndex < this.questions.length - 1) {
      this.currentQuestionIndex++;
      this.cdr.detectChanges();
      this.playAudio();
    }
  }

  async previousQuestion() {
    if (this.currentQuestionIndex > 0) {
      this.currentQuestionIndex--;
      this.cdr.detectChanges();
      this.playAudio();
    }
  }

  playAudio() {
    if (this.audioElement && this.audioElement.nativeElement) {
      this.audioElement.nativeElement.volume = 0.5; // Adjust volume
      this.audioElement.nativeElement.load();

      // Add event listener for when the audio ends
      this.audioElement.nativeElement.onended = () => {
        this.startRecording(); // Start recording when audio finishes
      };

      this.audioElement.nativeElement.play().then(() => {
        console.log('Audio playback started');
      }).catch(error => {
        console.error('Error playing audio:', error);
      });
    }
  }

  startRecording() {
    this.recording = true;
    const mediaConstraints = {
      video: false,
      audio: true,
    };
    navigator.mediaDevices
      .getUserMedia(mediaConstraints)
      .then(this.successCallback.bind(this), this.errorCallback.bind(this));
  }

  successCallback(stream: MediaStream) {
    const options: RecordRTC.Options = {
      mimeType: 'audio/wav', // Explicitly set the mimeType to 'audio/wav'
    };
    const StereoAudioRecorder = RecordRTC.StereoAudioRecorder;
    this.record = new StereoAudioRecorder(stream, options);
    this.record.record();
  }

  stopRecording() {
    this.recording = false;
    this.record.stop(this.processRecording.bind(this));
  }

  processRecording(blob: Blob) {
    this.url = URL.createObjectURL(blob);
    console.log('blob', blob);
    console.log('url', this.url);
    this.uploadAudio(blob);
  }

  async uploadAudio(audioBlob: Blob) {
    const audioFile = new File([audioBlob], `answer_${this.currentQuestionIndex}.wav`, { type: 'audio/wav' });
    const formData = new FormData();
    formData.append('audio_file', audioFile);
    formData.append('question_id', this.questions[this.currentQuestionIndex].question_id);

    try {
      await this.interviewService.uploadResponse(formData).toPromise();
      console.log('Audio response saved successfully.');
    } catch (error) {
      console.error('Error saving audio response:', error);
    }
  }

  setupCamera() {
    navigator.mediaDevices.getUserMedia({
      video: { width: 300, height: 250 },
      audio: false // Disable audio for video stream
    }).then(stream => {
      this.videoRef.nativeElement.srcObject = stream;

      // Log tracks to verify video
      console.log('Video tracks:', stream.getVideoTracks());
    }).catch(error => {
      console.error('Error accessing media devices.', error);
    });
  }

  sanitize(url: string) {
    return this.domSanitize.bypassSecurityTrustResourceUrl(url);
  }

  errorCallback(error: Error) {
    this.error = 'Can not play audio in your browser';
  }


  analyzeInterview() {
    this.isLoading = true;
    this.analysisMessage = 'Please be patient. The analysis process might take a while...';
    this.interviewService.analyzeInterview().subscribe(
      (response: any) => {
        console.log('Analysis results:', response.feedback_results);
        this.analysisMessage = 'Analysis complete! Here are your results:';
        // Handle the response, e.g., display feedback to the user
        this.isLoading = false;
        this.router.navigate(['/dashboard/result'], {
          state: { feedbackResults: response.feedback_results }
        });
      },
      (error) => {
        console.error('Error analyzing interview:', error);
        this.isLoading = false;
        this.analysisMessage = 'An error occurred during analysis. Please try again.';
      }
    );
  }
  toggleAudio() {
    const audio = this.audioElement.nativeElement; // Access the native element
    if (this.isAudioPlaying) {
        audio.pause(); // Now it should work
    } else {
        audio.play();
    }
    this.isAudioPlaying = !this.isAudioPlaying; // Toggle the state
}
}