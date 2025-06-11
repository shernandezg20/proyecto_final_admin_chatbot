import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-view-predictions',
  standalone: false,
  templateUrl: './view-predictions.component.html',
  styleUrl: './view-predictions.component.css'
})
export class ViewPredictionsComponent implements OnInit {
  predicciones: any[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.apiService.getPredicciones().subscribe(data => {
      this.predicciones = data;
    });
  }

  aceptar(id: number) {
    console.log('Aceptando id:', id);
    this.apiService.aceptarPrediccion(id).subscribe(() => {
      alert('Aceptado');
      this.ngOnInit();
    });
  }

  rechazar(id: number) {
    this.apiService.rechazarPrediccion(id).subscribe(() => {
      alert('Rechazado');
      this.ngOnInit();
    });
  }
}
