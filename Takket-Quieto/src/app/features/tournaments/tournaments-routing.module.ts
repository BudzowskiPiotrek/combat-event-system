import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Los componentes se añadirán en el siguiente paso.
const routes: Routes = [
    {
        path: '',
        children: [
            { path: '', redirectTo: 'list', pathMatch: 'full' },
            // { path: 'list', component: TournamentsListComponent },
            // { path: ':id', component: TournamentDetailComponent }
        ]
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class TournamentsRoutingModule { }
