import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Prediccion } from './prediccion.model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = 'http://localhost:8000'; // Cambia si usas proxy

  constructor(private http: HttpClient) {}

  getPredicciones(): Observable<Prediccion[]> {
    return this.http.get<Prediccion[]>(`${this.apiUrl}/predicciones`);
  }

  aceptarPrediccion(id: number) {
    return this.http.post(`${this.apiUrl}/predicciones/aceptar`, { id });
  }

  rechazarPrediccion(id: number) {
    return this.http.post(`${this.apiUrl}/predicciones/rechazar`, { id });
  }

  guardarPrecioFinal(data: {
  id_producto: number;
  id_prediccion: number;
  id_usuario: number;
  precio_final: number;
}) {
  return this.http.post(`${this.apiUrl}/guardar-precio-final`, data);
}

}
