import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { TournamentsService } from '../../../../core/services/tournaments.service';

@Component({
    standalone: false,
    selector: 'app-tournament-form',
    templateUrl: './tournament-form.component.html',
    styleUrls: ['./tournament-form.component.css']
})
export class TournamentFormComponent implements OnInit {
    tournamentForm: FormGroup;
    submitting = false;

    constructor(
        private fb: FormBuilder,
        private tournamentsService: TournamentsService,
        private router: Router
    ) {
        this.tournamentForm = this.fb.group({
            name: ['', [Validators.required, Validators.minLength(3)]]
        });
    }

    ngOnInit(): void { }

    onSubmit(): void {
        if (this.tournamentForm.valid) {
            this.submitting = true;
            this.tournamentsService.create(this.tournamentForm.value).subscribe({
                next: (createdTournament) => {
                    this.router.navigate(['/tournaments', createdTournament.id]);
                },
                error: (err) => {
                    console.error('Error creating tournament:', err);
                    this.submitting = false;
                }
            });
        }
    }

    onCancel(): void {
        this.router.navigate(['/tournaments']);
    }
}
