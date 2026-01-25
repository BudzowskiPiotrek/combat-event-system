import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TournamentsPageComponent } from './page-tournaments/tournaments-page.component';
import { TournamentFormComponent } from './components/tournament-form/tournament-form.component';
import { TournamentDetailPageComponent } from './page-tournament-detail/tournament-detail-page.component';

const routes: Routes = [
    { path: '', component: TournamentsPageComponent },
    { path: 'new', component: TournamentFormComponent },
    { path: ':id', component: TournamentDetailPageComponent }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class TournamentsRoutingModule { }
