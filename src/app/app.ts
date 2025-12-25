import { CommonModule } from '@angular/common';
import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { Network } from './network';

@Component({
  selector: 'app-root',
  imports: [CommonModule,FormsModule ],
  templateUrl: './app.html',
  styleUrl: './app.less'
})
export class App {

  constructor(private networkService:Network) {

  }
  protected readonly title = signal('employees-chatbot');
  messages: { type: string; question: string; answer: string }[] = [];
  userInput:any
  closeChat() {

  }

 sendMessage() {
  const text = (this.userInput || '').trim();
  if (!text) return;

  const msg = {
    type: 'user',
    question: text,
    answer: 'Typing...'
  };
  this.networkService.getData(text).subscribe((data:any) => {
    msg.answer = data
  })
  this.messages.push(msg);
  this.userInput = '';
}
}
