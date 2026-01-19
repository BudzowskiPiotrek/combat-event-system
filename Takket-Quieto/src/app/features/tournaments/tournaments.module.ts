import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { TournamentsRoutingModule } from './tournaments-routing.module';
import { TournamentsPageComponent } from './page-tournaments/tournaments-page.component';

@NgModule({
    declarations: [
        TournamentsPageComponent
    ],
    imports: [
        CommonModule,
        TournamentsRoutingModule
    ]
})
export class TournamentsModule { }
