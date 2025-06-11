// src/app/app.module.ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { UploadCsvComponent } from './components/upload-csv/upload-csv.component';
import { ViewPredictionsComponent } from './components/view-predictions/view-predictions.component';
import { RouterModule } from '@angular/router';
import { routes } from './app.routes';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { AdminComponent } from './admin/admin.component';


@NgModule({
  declarations: [AppComponent, 
    DashboardComponent, 
    UploadCsvComponent, 
    ViewPredictionsComponent, AdminComponent
  ],
  imports: [BrowserModule,
    RouterModule.forRoot(routes),
    HttpClientModule,
    FormsModule
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
