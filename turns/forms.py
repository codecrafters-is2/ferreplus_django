from django import forms
from .models import Appointment, TurnProposal, Branch, CancellationReport, Barter
from datetime import date, timedelta

class TurnProposalForm(forms.ModelForm):
    tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    date = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(
            attrs={
                "placeholder": ("Fecha"),
                "type": "date",
                "min": tomorrow,
                }
            ),
        )
    TIME_CHOICES = ([(f"{h:02d}:00", f"{h:02d}:00") for h in range(9, 20)])
    start_time = forms.ChoiceField(
        label="Rango horario desde",
        choices=TIME_CHOICES,
        widget=forms.Select()
    )
    end_time = forms.ChoiceField(
        label="hasta",
        choices=TIME_CHOICES,
        widget=forms.Select()
    )

    class Meta:
        model = TurnProposal
        fields = ['branch', 'start_time', 'end_time', 'date']
        labels = {"branch": "Sucursal"}

    def __init__(self, *args, **kwargs):
        super(TurnProposalForm, self).__init__(*args, **kwargs)
        self.fields['branch'].queryset = Branch.active_objects.all()
        for field_name, field in self.fields.items():
            field.required = True

    def clean(self):
        cleaned_data = super().clean()
        branch = cleaned_data.get("branch")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("La hora de inicio debe ser anterior a la hora de finalización.")
        return cleaned_data

class SelectTurnForm(forms.Form):
    turn_proposal = forms.ModelChoiceField(queryset=TurnProposal.objects.none())

    def __init__(self, barter, *args, **kwargs):
        super(SelectTurnForm, self).__init__(*args, **kwargs)
        self.fields['turn_proposal'].queryset = TurnProposal.objects.filter(barter=barter)



class AppointmentForm(forms.ModelForm):
    time = forms.ChoiceField(
        label="Hora",
        choices=[],
        widget=forms.Select()
    )

    class Meta:
        model = Appointment
        fields = ['time']

    def __init__(self, *args, **kwargs):
        turn_proposal = kwargs.pop('turn_proposal')
        branch = kwargs.pop('branch') 
        barter = kwargs.pop('barter')
        date = kwargs.pop('date')

        super(AppointmentForm, self).__init__(*args, **kwargs)

        start_hour = int(turn_proposal.start_time[:2])
        end_hour = int(turn_proposal.end_time[:2])
        TIME_CHOICES_APPOINTMENT = [
            (f"{h:02d}:00", f"{h:02d}:00") 
            for h in range(start_hour, end_hour)
        ]
        self.fields['time'].choices = TIME_CHOICES_APPOINTMENT

        self.instance.branch = branch
        self.instance.barter = barter
        self.instance.date = date 

class CancelBarterForm(forms.ModelForm):
    class Meta:
        model = CancellationReport
        fields = ['reason']
        labels = {'reason':''}

    def __init__(self, barter, *args, **kwargs):
        super().__init__(*args, **kwargs)