import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ReactiveFormsModule } from '@angular/forms';
import { TournamentsRoutingModule } from './tournaments-routing.module';
import { TournamentsPageComponent } from './page-tournaments/tournaments-page.component';
import { TournamentFormComponent } from './components/tournament-form/tournament-form.component';
import { TournamentDetailPageComponent } from './page-tournament-detail/tournament-detail-page.component';
import { ParticipantPickerComponent } from './components/participant-picker/participant-picker.component';
import { BracketViewComponent } from './components/bracket-view/bracket-view.component';
import { RoundColumnComponent } from './components/round-column/round-column.component';
import { MatchCardComponent } from './components/match-card/match-card.component';

@NgModule({
    declarations: [
        TournamentsPageComponent,
        TournamentFormComponent,
        TournamentDetailPageComponent,
        ParticipantPickerComponent,
        BracketViewComponent,
        RoundColumnComponent,
        MatchCardComponent
    ],
    imports: [
        CommonModule,
        ReactiveFormsModule,
        TournamentsRoutingModule
    ]
})
export class TournamentsModule { }
