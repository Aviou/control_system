from django import forms

PHASE_CHOICES = [
    ('keimung', 'Keimungsphase'),
    ('wachstum', 'Wachstumsphase'),
    ('bluete', 'Blütephase'),
]

class MoistureForm(forms.Form):
    phase = forms.ChoiceField(label='Phase', choices=PHASE_CHOICES)