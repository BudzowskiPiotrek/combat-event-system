import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ReactiveFormsModule } from '@angular/forms';
import { TournamentsRoutingModule } from './tournaments-routing.module';
import { TournamentsPageComponent } from './page-tournaments/tournaments-page.component';
import { TournamentFormComponent } from './components/tournament-form/tournament-form.component';
import { TournamentDetailPageComponent } from './page-tournament-detail/tournament-detail-page.component';

@NgModule({
    declarations: [
        TournamentsPageComponent,
        TournamentFormComponent,
        TournamentDetailPageComponent
    ],
    imports: [
        CommonModule,
        ReactiveFormsModule,
        TournamentsRoutingModule
    ]
})
export class TournamentsModule { }
