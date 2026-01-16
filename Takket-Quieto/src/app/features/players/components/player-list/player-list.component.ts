import { Component, Input } from '@angular/core';
import { Player } from '../../models/player.model';


@Component({
    selector: 'app-player-list',
    templateUrl: './player-list.component.html',
    styleUrls: ['./player-list.component.css']
})
export class PlayerListComponent {
    @Input() players: Player[] = [];
}

