from django.db import models
from barter.models import Barter
from branches.models import Branch
from accounts.models import CustomUser

class TurnProposal(models.Model):
    barter = models.ForeignKey(Barter, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    start_time = models.CharField(max_length=5, null=True)
    end_time = models.CharField(max_length=5, null=True)
    proposer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    selected = models.BooleanField(default=False)

    def __str__(self) :
        return f"{self.branch}\n Día: {self.date}\n Entre las {self.start_time} y las {self.end_time}"

class Appointment(models.Model):
    barter = models.OneToOneField(Barter, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self) :
        return f"{self.branch}\n Día: {self.date}\n {self.time} horas."
    
class CancellationReport(models.Model):
    barter = models.ForeignKey(Barter, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self) :
        return f"{self.barter}"