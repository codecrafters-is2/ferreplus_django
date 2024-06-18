from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth, TruncMonth
from django.http import JsonResponse
from barter.models import Barter
from accounts.models import EmployeeUser
from branches.models import Branch

MONTHS_NAMES = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]

class BarterCharts:
    def info_chart_1(self, year):
        values = [0] * 12
        barters_per_month = list(
            Barter.objects.filter(finished_date__year=year)
            .annotate(month=TruncMonth("finished_date"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
            .values("month", "count")
        )
        # Preparar los datos para el gráfico
        month_nums = [barter["month"].month for barter in barters_per_month]
        for i in range(len(month_nums)):
            values[month_nums[i]] = barters_per_month[i]["count"]
        return MONTHS_NAMES, values

    def info_chart_2(self):
        states_names = {
            "accepted": "Aceptados",
            "cancelled":"Cancelados",
            "committed":"Finalizados",
            "requested":"Solicitados",
            "parcial_accepted":"Parcialmente Aceptados"
        }
        barter_states_count = list(
            Barter.objects.values("state").annotate(count=Count("id")).order_by("state")
        )

        labels = []
        data = []
        for state_count in barter_states_count:
            state_name = states_names[state_count["state"]]
            # state_name = dict(BARTER_STATE_CHOICES).get(state_value, "Unknown")
            labels.append(state_name)
            data.append(state_count["count"])

        return labels, data

    def info_chart_3(self):
        barter_branch_count = list(
            Barter.objects.values("branch").annotate(count=Count("id"))
        )

        labels = []
        data = []
        for branch_count in barter_branch_count:
            branch = branch_count["branch"]
            if branch is not None:
                branch_obj = Branch.objects.get(id=branch)
                labels.append(str(branch_obj))
            else:
                labels.append("No branch")
            data.append(branch_count["count"])

        return labels, data


class IncomeCharts:
    def info_chart_1(self, year):
        values = [0] * 12
        barters_per_month = list(
            Barter.objects.filter(finished_date__year=year)
            .annotate(month=TruncMonth("finished_date"))
            .values("month")
            .annotate(total_income=Sum("income"))
            .order_by("month")
            .values("month", "total_income")
        )

        # Preparar los datos para el gráfico
        for barter in barters_per_month:
            month = barter["month"].month - 1  # Subtract 1 to convert to 0-indexed
            values[month] = (
                float(barter["total_income"]) if barter["total_income"] else 0.0
            )

        return MONTHS_NAMES, values
