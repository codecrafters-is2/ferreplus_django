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
    labels_5, data_5 = barter_charts.info_chart_5()

    context = {
        "chart_2": {
            "labels": labels_2,
            "data": data_2,
        },
        "chart_3":{
            "labels": labels_3,
            "data": data_3,
        },
        "chart_5":{
        "labels": labels_5, "data": data_5
        }
    }

    if request.method == "POST":
        year = request.POST.get("year")
        if year:
            labels_1, values_1 = barter_charts.info_chart_1(year=year)

            context["chart_1"] = {
                "labels": labels_1,
                "data": values_1,
                "selected_year": year,
            }

            labels_4, values_4 = barter_charts.number_finished_barters(year=year)
            context["chart_4"] = {
                "labels": labels_4,
                "data": values_4,
                "selected_year": year,
            }

            labels_6, values_6 = barter_charts.info_chart_6(year=year)
            context["chart_6"] = {
                "labels": labels_6,
                "data": values_6,
                "selected_year": year,
            }

    return render(request, "metrics-report/barter_report.html", context)


def income_chart_view(request):
    income_charts = IncomeCharts()
    context={}

    if request.method == "POST":
        year = request.POST.get("year")
        if year:
            labels_1, values_1 = income_charts.barter_income_per_month(year=year)
            context["barter_income_month"] = {
                "labels": labels_1,
                "data": values_1,
                "selected_year": year,
            }
            labels_2, values_2 = income_charts.barter_income_per_branch(year=year)
            context["barter_income_branches"]={
                "labels": labels_2,
                "data": values_2,
                "selected_year": year
            }
            labels_3, values_3 = income_charts.package_income_per_month(year=year)
            context["package_income_month"] = {
                "labels": labels_3,
                "data": values_3,
                "selected_year": year,
            }
            labels_4, values_4 = income_charts.income_per_package(year=year)
            context["package_name_income"] = {
                "labels": labels_4,
                "data": values_4,
                "selected_year": year,
            }

    return render(request, "metrics-report/income_report.html", context)
