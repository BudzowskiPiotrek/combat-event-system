import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Player } from '../../../../models/player.model';


@Component({
    standalone: false,
    selector: 'app-player-list',
    templateUrl: './player-list.component.html',
    styleUrls: ['./player-list.component.css']
})
export class PlayerListComponent {
    @Input() players: Player[] = [];
    @Output() edit = new EventEmitter<number>();
    @Output() toggle = new EventEmitter<number>();

    onEdit(id: number): void {
        this.edit.emit(id);
    }

    onToggle(id: number): void {
        this.toggle.emit(id);
    }
}

