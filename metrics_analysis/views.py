from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth, TruncMonth
from django.http import JsonResponse
from barter.models import Barter
from accounts.models import EmployeeUser
from branches.models import Branch
from .utils import BarterCharts, IncomeCharts


class MetricsView(TemplateView):
    template_name = "metrics-report/metrics_analysis.html"


def barter_chart_view(request):
    barter_charts = BarterCharts()
    labels_2, data_2 = barter_charts.info_chart_2()
    labels_3, data_3 = barter_charts.info_chart_3()
    context = {
        "chart_2": {
            "labels": labels_2,
            "data": data_2,
        },
        "chart_3":{
            "labels": labels_3,
            "data": data_3,
        }
    }

    if request.method == "POST":
        year = request.POST.get("year")
        if year:
            labels, values = barter_charts.info_chart_1(year=year)

            context["chart_1"] = {
                "labels": labels,
                "data": values,
                "selected_year": year,
            }

    return render(request, "metrics-report/barter_report.html", context)


def income_chart_view(request):
    income_charts = IncomeCharts()

    context={}
    ## labels_2, data_2 = info_chart_2()
    ## labels_3, data_3 = info_chart_3()
    ## context = {
    ##    "chart_2": {
    ##        "labels": labels_2,
    ##        "data": data_2,
    ##    },
    ##    "chart_3": {
    ##        "labels": labels_3,
    ##        "data": data_3,
    ##    },
    ## }
    #
    if request.method == "POST":
        year = request.POST.get("year")
        if year:
            labels, values = income_charts.info_chart_1(year=year)

            context["chart_1"] = {
                "labels": labels,
                "data": values,
                "selected_year": year,
            }

    return render(request, "metrics-report/income_report.html", context)
