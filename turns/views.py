from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect, render
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from .models import Barter, TurnProposal, Appointment
from accounts.models import EmployeeUser
from .forms import TurnProposalForm, AppointmentForm, CancelBarterForm
from accounts.mixins import ClientRequiredMixin, EmployeeRequiredMixin
from django.views.generic import TemplateView, CreateView, View, DeleteView
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.http import JsonResponse

class ProposeTurnsView(ClientRequiredMixin, FormView):
    template_name = 'turns/propose_turns.html'

    def get_success_url(self) -> str:
        barter_id = self.kwargs['barter_id']
        return reverse_lazy('turns_list', kwargs={'barter_id': barter_id})
    
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
        if (barter.state != 'parcial_accepted'):
            barter.change_state('parcial_accepted')
        instances = formset.save(commit=False)
        for instance in instances:
            instance.barter = barter
            instance.proposer = self.request.user
            instance.save()
        return super().form_valid(formset)
    
    def post(self, request, *args, **kwargs):
        selected_barter_id = request.POST.get('barter_id')
        if selected_barter_id:
            return redirect('propose_turns', barter_id=selected_barter_id)
        return super().post(request, *args, **kwargs)
    
class TurnsListView(ClientRequiredMixin, TemplateView):
    model = TurnProposal
    template_name = 'turns/turns_list.html'
    context_object_name = 'turns'

    def get_queryset(self):
        user = self.request.user
        barter_id = self.kwargs['barter_id']
        return self.filter_turn_proposals(user, barter_id)

    def filter_turn_proposals(self, user, barter_id):
        return TurnProposal.objects.filter(
            Q(barter__requesting_post__author=user) | Q(barter__requested_post__author=user),
            Q(barter__id=barter_id)
        )

    def post(self, request, *args, **kwargs):
        selected_turn_id = request.POST.get('selected_turn_id')
        if selected_turn_id:
            return self.handle_selected_turn(selected_turn_id)
        return super().post(request, *args, **kwargs)

    @require_POST
    def handle_selected_turn(self, selected_turn_id):
        return redirect('select-turn', turn_id=selected_turn_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        barter_id = self.kwargs['barter_id']
        turns = self.filter_turn_proposals(user, barter_id)
        barter = get_object_or_404(Barter, id=barter_id)
        context['proposer'] = barter.requested_post.author
        context['turns'] = turns
        context['barter_id'] = barter_id
        return context

class AppointmentCreateView(ClientRequiredMixin, FormView, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'turns/select-turn.html'
    success_url = reverse_lazy('appointment_success')

    def form_valid(self, form):
        barter = self.get_form_kwargs()['barter']
        form.instance.barter = barter
        barter.change_state('accepted')
        form.instance.date = self.get_form_kwargs()['date']
        branch = self.get_form_kwargs()['branch']
        form.instance.branch = branch
        barter.accept(branch)
        appointment = form.save(commit=False)
        appointment.save()
        TurnProposal.objects.filter(barter=barter).delete()
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

class AppointmentListView(ClientRequiredMixin,TemplateView):
    model = Appointment
    template_name = 'turns/appointments_list.html'
    context_object_name = 'appointments'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(
            Q(barter__requesting_post__author=user) | Q(barter__requested_post__author=user)
        ) 
        return context
    
class EmployeeAppointmentListView(EmployeeRequiredMixin,TemplateView):
    model = Appointment
    template_name = 'turns/employee_appointments_list.html'
    context_object_name = 'appointments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = EmployeeUser.objects.get(id=self.kwargs['employee_id'])
        employee_branch = employee.branch
        context['appointments'] = Appointment.objects.filter(branch=employee_branch, barter__state='accepted')
        return context
    
class RegisterBarterView(EmployeeRequiredMixin, View):
    model = Barter
    def post(self, request, *args, **kwargs):
        barter_id = kwargs.get('barter_id')
        barter = get_object_or_404(Barter, id=barter_id)
        employee_id = kwargs.get('employee_id')
        employee = get_object_or_404(EmployeeUser, id=employee_id)
        barter.register(employee)
        Appointment.objects.filter(barter=barter).delete()
        return redirect('barter_finished', employee_id)
    
class ConfirmCommittedBarterView(EmployeeRequiredMixin, View):
    template_name = 'turns/confirm_committed_barter.html'

    def post(self, request, *args, **kwargs):
        barter_id = kwargs.get('barter_id')
        employee_id = kwargs.get('employee_id')
        barter = get_object_or_404(Barter, id=barter_id)
        employee = get_object_or_404(EmployeeUser, id=employee_id)
        return render(request, self.template_name, {
            'barter_id': barter_id,
            'employee_id': employee_id,
            'barter': barter,
            'employee': employee
        })
    
class EmployeeBarterCancelView(EmployeeRequiredMixin, FormView):
    model = Barter
    form_class = CancelBarterForm
    template_name = "barter/employee_cancel_barter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.get_employee_object()
        context['barter'] = self.get_barter_object()
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('employee_appointments_list', kwargs={'employee_id':self.kwargs['employee_id']})

    def get_barter_object(self):
        return get_object_or_404(Barter, pk=self.kwargs['barter_id'])
    
    def get_employee_object(self):
        return get_object_or_404(EmployeeUser, pk=self.kwargs['employee_id'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['barter'] = self.get_barter_object()
        return kwargs

    def form_valid(self, form):
        report = form.save(commit=False)
        barter = self.get_barter_object()
        report.barter = barter
        employee = self.get_employee_object()
        barter.employee = employee
        report.save()
        barter.delete()
        Appointment.objects.filter(barter=barter).delete()
        return super().form_valid(form)