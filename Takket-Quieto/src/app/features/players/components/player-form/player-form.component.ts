import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { PlayersService } from '../../../../core/services/players.service';

/**
 * Componente de formulario para crear/editar jugadores.
 * Responsabilidad: Manejar entrada de datos y validacion.
 */
@Component({
    standalone: false,
    selector: 'app-player-form',
    templateUrl: './player-form.component.html',
    styleUrls: ['./player-form.component.css']
})
export class PlayerFormComponent implements OnInit {
    playerForm: FormGroup;
    submitting = false;
    isEditMode = false;
    playerId: number | null = null;

    constructor(
        private fb: FormBuilder,
        private playersService: PlayersService,
        private router: Router,
        private route: ActivatedRoute
    ) {
        this.playerForm = this.fb.group({
            nick: ['', [Validators.required, Validators.minLength(3)]],
            logoUrl: [''],
            active: [true]
        });
    }

    ngOnInit(): void {
        const id = this.route.snapshot.paramMap.get('id');
        if (id) {
            this.isEditMode = true;
            this.playerId = Number(id);
            this.loadPlayer(this.playerId);
        }
    }

    loadPlayer(id: number): void {
        this.playersService.getById(id).subscribe({
            next: (player) => {
                this.playerForm.patchValue({
                    nick: player.nick,
                    logoUrl: player.logoUrl,
                    active: player.active
                });
            },
            error: (err) => {
                console.error('Error loading player:', err);
                this.router.navigate(['/players']);
            }
        });
    }

    onSubmit(): void {
        if (this.playerForm.invalid) {
            this.playerForm.markAllAsTouched();
            return;
        }

        this.submitting = true;

        if (this.isEditMode && this.playerId) {
            const player = { ...this.playerForm.value, id: this.playerId };
            this.playersService.update(player).subscribe({
                next: () => this.handleSuccess(),
                error: (err) => this.handleError(err)
            });
        } else {
            this.playersService.create(this.playerForm.value).subscribe({
                next: () => this.handleSuccess(),
                error: (err) => this.handleError(err)
            });
        }
    }

    handleSuccess(): void {
        this.submitting = false;
        this.router.navigate(['/players']);
    }

    handleError(err: any): void {
        console.error('Error saving player:', err);
        this.submitting = false;
    }

    onCancel(): void {
        this.router.navigate(['/players']);
    }
}
