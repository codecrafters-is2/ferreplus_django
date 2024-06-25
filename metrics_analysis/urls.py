from django.urls import path
from .views import MetricsView, barter_chart_view, income_chart_view

urlpatterns = [
    path("", MetricsView.as_view(), name="metrics"),
    path("barter_chart/", barter_chart_view, name="barter_chart"),
    path("income_charts/", income_chart_view, name="income_charts"),
]
