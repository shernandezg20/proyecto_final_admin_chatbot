import { Component, OnInit } from '@angular/core';
import { AdminService } from './admin.service';
import { Prediccion } from './prediccion.model';
import { Chart } from 'chart.js/auto';

@Component({
  selector: 'app-admin',
  standalone: false,
  templateUrl: './admin.component.html',
  styleUrl: './admin.component.css'
})
export class AdminComponent implements OnInit {
  predicciones: Prediccion[] = [];

  constructor(private adminService: AdminService) {}

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.adminService.getPredicciones().subscribe(data => {
      this.predicciones = data;
      this.loadChart(data);
    });
  }

  aceptar(id: number) {
    this.adminService.aceptarPrediccion(id).subscribe(() => this.loadData());
  }

  rechazar(id: number) {
    this.adminService.rechazarPrediccion(id).subscribe(() => this.loadData());
  }

  loadChart(data: Prediccion[]) {
    const nombres = data.map(p => p.nombre);
    const predichos = data.map(p => p.precio_predicho);
    const oficiales = data.map(p => p.precio_real ?? 0);

    new Chart('prediccionChart', {
      type: 'bar',
      data: {
        labels: nombres,
        datasets: [
          {
            label: 'Precio Predicho',
            data: predichos,
            backgroundColor: 'rgba(54, 162, 235, 0.6)'
          },
          {
            label: 'Precio Oficial',
            data: oficiales,
            backgroundColor: 'rgba(255, 99, 132, 0.6)'
          }
        ]
      }
    });
  }

  guardarPrecio(p: Prediccion) {
  const id_usuario = 1; // Obtener dinámicamente en versión final
  this.adminService.guardarPrecioFinal({
    id_producto: p.id_producto,
    id_prediccion: p.id_prediccion,
    id_usuario,
    precio_final: p.precio_real
  }).subscribe(() => {
    alert('Precio final guardado');
    this.loadData();
  });
}

}