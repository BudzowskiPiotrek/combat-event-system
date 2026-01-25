import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PlayersPageComponent } from './page-player/players-page.component';
import { PlayerFormComponent } from './components/player-form/player-form.component';

const routes: Routes = [
    { path: '', component: PlayersPageComponent },
    { path: 'new', component: PlayerFormComponent },
    { path: 'edit/:id', component: PlayerFormComponent }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class PlayersRoutingModule { }
