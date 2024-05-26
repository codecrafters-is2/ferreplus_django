from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from .models import Barter, TurnProposal, Appointment
from .forms import TurnProposalForm, AppointmentForm
from accounts.mixins import ClientRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.db.models import Q

class ProposeTurnsView(ClientRequiredMixin, FormView):
    template_name = 'turns/propose_turns.html'
    success_url = reverse_lazy('turns_list')
    
    def get_form_class(self):
        return modelformset_factory(TurnProposal, form=TurnProposalForm, extra=1)

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
    
    def post(self, request, *args, **kwargs):
        selected_barter_id = request.POST.get('selected_barter_id')
        if selected_barter_id:
            return redirect('propose_turns', barter_id=selected_barter_id)
        return super().post(request, *args, **kwargs)
    
class TurnsListView(ClientRequiredMixin, TemplateView):
    model = TurnProposal
    template_name = 'turns/turns_list.html'
    context_object_name = 'turns'

    def get_queryset(self):
        user = self.request.user
        return TurnProposal.objects.filter(
            Q(barter__requesting_post__author=user) | Q(barter__requested_post__author=user)
        )
    
    def post(self, request, *args, **kwargs):
        selected_turn_id = request.POST.get('selected_turn_id')
        if selected_turn_id:
            return redirect('select-turn', turn_id=selected_turn_id)
        return super().post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        turns = self.get_queryset()
        context['turns'] = turns
        context['barter_id'] = self.get_barter_id(turns)
        return context
    
    def get_barter_id(self, turns):
        return turns.first().barter.id


class AppointmentCreateView(ClientRequiredMixin, FormView, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'turns/select-turn.html'
    success_url = reverse_lazy('appointment_success')

    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        turn_proposal = TurnProposal.objects.get(id=self.kwargs['turn_proposal_id'])
        kwargs['turn_proposal'] = turn_proposal
        kwargs['branch'] = turn_proposal.branch
        kwargs['barter'] = turn_proposal.barter
        kwargs['date'] = turn_proposal.date
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        turn_proposal = TurnProposal.objects.get(id=self.kwargs['turn_proposal_id'])
        context['turn_proposal'] = turn_proposal
        return context
    
class AppointmentCreateSuccessView(ClientRequiredMixin,TemplateView):
    template_name = 'temp_messages/appointment_created.html'