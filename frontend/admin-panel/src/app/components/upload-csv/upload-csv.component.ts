import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-upload-csv',
  standalone: false,
  templateUrl: './upload-csv.component.html',
  styleUrl: './upload-csv.component.css'
})
export class UploadCsvComponent {
  selectedFile: File | null = null;

  constructor(private apiService: ApiService) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  upload() {
    if (this.selectedFile) {
      this.apiService.uploadCSV(this.selectedFile).subscribe(response => {
        alert('Archivo subido correctamente');
      });
    }
  }
}
