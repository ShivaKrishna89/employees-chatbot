import { CommonModule } from '@angular/common';
import { Component, signal, ViewChild, ElementRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { Network } from './network';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-root',
  imports: [CommonModule,FormsModule ],
  templateUrl: './app.html',
  styleUrl: './app.less'
})
export class App {
@ViewChild('attachmentInput') attachmentInput!: ElementRef<HTMLInputElement>;

  constructor(private networkService:Network) {

  }
  protected readonly title = signal('employees-chatbot');
  messages: { type: string; question: string; answer: string }[] = [];
  userInput:any
  selectedFile: File | null = null;

  closeChat() {

  }

onFileSelected(event: Event) {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files.length > 0) {
    this.selectedFile = input.files[0];
  }
}


 clearFile() {
  this.selectedFile = null;

  if (this.attachmentInput) {
    this.attachmentInput.nativeElement.value = '';
  }
}

  sendMessage() {
  const text = (this.userInput || '').trim();
  if (!text && !this.selectedFile) return;

  const msg = {
    type: 'user',
    question: text + (this.selectedFile ? `<br>[File: ${this.selectedFile.name} attachment]` : ''),
    answer: 'Typing...'
  };

  // ✅ PUSH IMMEDIATELY
  this.messages.push(msg);

  if (this.selectedFile) {
    this.networkService.uploadFile(this.selectedFile, text)
      .pipe(finalize(() => this.clearFile()))
      .subscribe(
        (data: any) => {
          msg.answer = data.response || data;
        },
        () => {
          msg.answer = 'Error uploading file';
        }
      );
  } else {
    this.networkService.getData(text).subscribe(
      (data: any) => {
        msg.answer = data;
      },
      () => {
        msg.answer = 'Error';
      }
    );
  }

  this.userInput = '';
}

}

