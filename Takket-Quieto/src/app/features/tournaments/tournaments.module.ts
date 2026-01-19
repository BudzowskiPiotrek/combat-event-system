import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ReactiveFormsModule } from '@angular/forms';
import { TournamentsRoutingModule } from './tournaments-routing.module';
import { TournamentsPageComponent } from './page-tournaments/tournaments-page.component';
import { TournamentFormComponent } from './components/tournament-form/tournament-form.component';

@NgModule({
    declarations: [
        TournamentsPageComponent,
        TournamentFormComponent
    ],
    imports: [
        CommonModule,
        ReactiveFormsModule,
        TournamentsRoutingModule
    ]
})
export class TournamentsModule { }
