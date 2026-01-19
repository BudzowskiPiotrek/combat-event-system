import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TournamentsPageComponent } from './page-tournaments/tournaments-page.component';

const routes: Routes = [
    { path: '', component: TournamentsPageComponent },
    { path: ':id', component: TournamentsPageComponent } // Placeholder for detail
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class TournamentsRoutingModule { }
