from django.urls import path
from .views import ProposeTurnsView, SelectTurnView

urlpatterns = [
    path('barter/<int:barter_id>/propose_turns/', ProposeTurnsView.as_view(), name='propose_turns'),
    path('barter/<int:barter_id>/select_turn/', SelectTurnView.as_view(), name='select_turn'),
]
