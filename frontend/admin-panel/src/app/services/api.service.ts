import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private BASE_URL = 'http://localhost:8000'; // FastAPI corriendo localmente

  constructor(private http: HttpClient) {}

  uploadCSV(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.BASE_URL}/predicciones/upload-csv`, formData);
  }

  getPredicciones(): Observable<any[]> {
    return this.http.get<any[]>(`${this.BASE_URL}/predicciones`);
  }

  aceptarPrediccion(id: number): Observable<any> {
    return this.http.post(`${this.BASE_URL}/predicciones/aceptar`, { id });
  }

  rechazarPrediccion(id: number): Observable<any> {
    return this.http.post(`${this.BASE_URL}/predicciones/rechazar`, { id });
  }
}
