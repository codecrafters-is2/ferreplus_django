from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from .models import Barter, TurnProposal
from .forms import TurnProposalForm, SelectTurnForm
from accounts.mixins import ClientRequiredMixin

class ProposeTurnsView(ClientRequiredMixin, FormView):
    template_name = 'turns/propose_turns.html'
    form_class = modelformset_factory(TurnProposal, form=TurnProposalForm, extra=1)
    success_url = reverse_lazy('my_barters')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['barter'] = get_object_or_404(Barter, id=self.kwargs['barter_id'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'queryset': TurnProposal.objects.none()})
        return kwargs

    def form_valid(self, formset):
        barter = get_object_or_404(Barter, id=self.kwargs['barter_id'])
        instances = formset.save(commit=False)
        for instance in instances:
            instance.barter = barter
            instance.proposer = self.request.user
            instance.save()
        return super().form_valid(formset)

class SelectTurnView(ClientRequiredMixin, FormView):
    template_name = 'turns/select_turn.html'
    form_class = SelectTurnForm
    success_url = reverse_lazy('my_barters')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        barter = get_object_or_404(Barter, id=self.kwargs['barter_id'])
        kwargs.update({'barter': barter})
        return kwargs

    def form_valid(self, form):
        selected_turn = form.cleaned_data['turn_proposal']
        selected_turn.selected = True
        selected_turn.save()
        return super().form_valid(form)
