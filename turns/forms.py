from django import forms
from .models import Barter, Appointment, TurnProposal


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['branch', 'date', 'time']

class TurnProposalForm(forms.ModelForm):
    start_time = forms.TimeField(label='Rango horario')
    end_time = forms.TimeField(label='-')
    date = forms.DateField(label='Fecha')
    branch = forms.CharField(label='Sucursal')

    class Meta:
        model = TurnProposal
        fields = ['start_time', 'end_time', 'date', 'branch']

class SelectTurnForm(forms.Form):
    turn_proposal = forms.ModelChoiceField(queryset=TurnProposal.objects.none())

    def __init__(self, barter, *args, **kwargs):
        super(SelectTurnForm, self).__init__(*args, **kwargs)
        self.fields['turn_proposal'].queryset = TurnProposal.objects.filter(barter=barter)
