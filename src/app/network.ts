import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class Network {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getData(userInput: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/chat`, {
      params: { userInput }
    });
  }

  uploadFile(file: File, userInput: string = ''): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    if (userInput) {
      formData.append('userInput', userInput);
    }
    return this.http.post(`${this.baseUrl}/upload`, formData);
  }
}
