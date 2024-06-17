from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth, TruncMonth
from django.http import JsonResponse

from barter.models import Barter
from .utils import (
    months,
    colorPrimary,
    colorSuccess,
    colorDanger,
    generate_color_palette,
    get_year_dict,
)


class MetricsView(TemplateView):
    template_name = "metrics-report/metrics_analysis.html"


def barter_chart_view(request):
    if request.method == "POST":
        year = request.POST.get("year")
        if year:
            # Obtener la cantidad de trueques por mes para el año seleccionado
            barters_per_month = list(
                Barter.objects.filter(finished_date__year=year)
                .annotate(month=TruncMonth("finished_date"))
                .values("month")
                .annotate(count=Count("id"))
                .order_by("month")
                .values("month", "count")
            )

            # Preparar los datos para el gráfico
            labels = [barter["month"].strftime("%B") for barter in barters_per_month]
            data = [barter["count"] for barter in barters_per_month]

            context = {"labels": labels, "data": data, "selected_year": year}
            return render(request, "metrics-report/barter_report.html", context)

    # Renderizar la plantilla sin datos si no se ha seleccionado un año
    return render(request, "metrics-report/barter_report.html")
