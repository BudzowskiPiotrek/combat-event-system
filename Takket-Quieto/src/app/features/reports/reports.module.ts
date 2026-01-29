import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { LeaderboardComponent } from './pages/leaderboard/leaderboard.component';
import { HistoryComponent } from './pages/history/history.component';

const routes: Routes = [
    { path: 'leaderboard', component: LeaderboardComponent },
    { path: 'history', component: HistoryComponent },
    { path: '', redirectTo: 'leaderboard', pathMatch: 'full' }
];

@NgModule({
    declarations: [
        LeaderboardComponent,
        HistoryComponent
    ],
    imports: [
        CommonModule,
        FormsModule,
        RouterModule.forChild(routes)
    ]
})
export class ReportsModule { }
