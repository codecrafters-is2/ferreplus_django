from django.urls import path
from .views import ProposeTurnsView, TurnsListView, AppointmentCreateView, AppointmentCreateSuccessView

urlpatterns = [
    path('barter/<int:barter_id>/propose_turns/', ProposeTurnsView.as_view(), name='propose_turns'),
    path('appintment/<int:turn_proposal_id>/', AppointmentCreateView.as_view(), name='select-turn'),
    path('list', TurnsListView.as_view(), name='turns_list' ),
    path('', AppointmentCreateSuccessView.as_view(), name='appointment_success'),
]
