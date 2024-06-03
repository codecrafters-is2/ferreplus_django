from django.urls import path
from .views import (ProposeTurnsView,
                    TurnsListView, 
                    AppointmentCreateView, 
                    AppointmentCreateSuccessView, 
                    AppointmentListView, 
                    EmployeeAppointmentListView,
                    RegisterBarterView,
                    EmployeeBarterCancelView,
                    ConfirmCommittedBarterView,
                    )

urlpatterns = [
    path('barter/<int:barter_id>/propose_turns/', ProposeTurnsView.as_view(), name='propose_turns'),
    path('appointment/<int:turn_proposal_id>/', AppointmentCreateView.as_view(), name='select-turn'),
    path('list/<int:barter_id>/', TurnsListView.as_view(), name='turns_list' ),
    path('', AppointmentCreateSuccessView.as_view(), name='appointment_success'),
    path('appointments/', AppointmentListView.as_view(), name='appointments_list'),
    path('employee_appointments/<int:employee_id>/', EmployeeAppointmentListView.as_view(), name='employee_appointments_list'),
    path('register_barter/<int:barter_id>/<int:employee_id>', RegisterBarterView.as_view(), name='register_barter'),
    path('cancel_barter/<int:barter_id>/<int:employee_id>/', EmployeeBarterCancelView.as_view(), name='employee_cancel_barter'),
    path('confirm_committed_barter/<int:barter_id>/<int:employee_id>', ConfirmCommittedBarterView.as_view(), name='confirm_committed_barter'),
]
