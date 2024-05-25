from django.db import models
from barter.models import Barter
from branches.models import Branch
from accounts.models import CustomUser

class TurnProposal(models.Model):
    barter = models.ForeignKey(Barter, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.TimeField()
    proposer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    selected = models.BooleanField(default=False)

class Appointment(models.Model):
    barter = models.OneToOneField(Barter, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.TimeField()