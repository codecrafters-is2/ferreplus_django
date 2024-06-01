from django.contrib import admin
from .models import Appointment, TurnProposal, CancellationReport

admin.site.register(Appointment)
admin.site.register(TurnProposal)
admin.site.register(CancellationReport)
