import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { UploadCsvComponent } from './components/upload-csv/upload-csv.component';
import { ViewPredictionsComponent } from './components/view-predictions/view-predictions.component';
import { AdminComponent } from './admin/admin.component';

export const routes: Routes = [
    { path: '', component: DashboardComponent },
    { path: 'upload-csv', component: UploadCsvComponent },
    { path: 'view-predictions', component: ViewPredictionsComponent },
    { path: 'app-admin', component: AdminComponent},
    { path: '**', redirectTo: '' }
    ];
