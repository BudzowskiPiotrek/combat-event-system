import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

import { PlayersRoutingModule } from './players-routing.module';
import { PlayersPageComponent } from './page-player/players-page.component';
import { PlayerListComponent } from './components/player-list/player-list.component';

import { PlayerFormComponent } from './components/player-form/player-form.component';

@NgModule({
    declarations: [
        PlayersPageComponent,
        PlayerListComponent,

        PlayerFormComponent
    ],
    imports: [
        CommonModule,
        ReactiveFormsModule,
        PlayersRoutingModule
    ]
})
export class PlayersModule { }
