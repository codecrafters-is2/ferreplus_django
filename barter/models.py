from django.db import models
from posts.models import Post
from branches.models import Branch
from accounts.models import EmployeeUser
import datetime

class Barter(models.Model):
    BARTER_STATE_REQUESTED = 'requested'
    BARTER_STATE_ACCEPTED = 'accepted'
    BARTER_STATE_PARCIAL_ACCEPTED = 'parcial_accepted'
    BARTER_STATE_COMMITTED = 'committed'
    BARTER_STATE_CANCELLED = 'cancelled'
    BARTER_STATE_CHOICES = (
        (BARTER_STATE_REQUESTED, 'Solicitado'),
        (BARTER_STATE_ACCEPTED, 'Aceptado'),
        (BARTER_STATE_COMMITTED, 'Finalizado'),
        (BARTER_STATE_CANCELLED, 'Cancelado'),
        (BARTER_STATE_PARCIAL_ACCEPTED, 'Parcialmente Aceptado'),
    )
    requesting_post = models.ForeignKey(Post, related_name='requesting_barters', on_delete=models.SET_NULL, null=True)
    requested_post = models.ForeignKey(Post, related_name='requested_barters', on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, related_name='barter_branch', on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=20, choices=BARTER_STATE_CHOICES, default=BARTER_STATE_REQUESTED,) 
    employee = models.ForeignKey(EmployeeUser, related_name='barter_employee', on_delete=models.SET_NULL, null=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    finished_date = models.DateField(auto_now=False, null=True)  

    def delete(self):
        self.state = self.BARTER_STATE_CANCELLED
        self.requested_post.free_post()
        self.requesting_post.free_post()
        self.save()

    def change_state(self, state):
        self.state = state
        self.save()

    def accept(self, branch):
        self.state = 'accepted'
        self.branch = branch
        self.requested_post.reserve_post()
        self.requesting_post.reserve_post()
        self.save()

    def register(self, employee, income=0):
        self.change_state('committed')
        self.employee = employee
        self.income = income
        self.requested_post.complete_post()
        self.requesting_post.complete_post()
        # Registra la fecha en que el trueque fue registrado como finalizado por el empleado
        self.finished_date = datetime.date.today()  
        self.save()

    def get_cancellation_report(self):
        from turns.models import CancellationReport
        try:
            return self.cancellationreport_set.get()
        except CancellationReport.DoesNotExist:
            return None 

    def __str__(self) -> str:
        return self.requested_post.title +" x "+ self.requesting_post.title
