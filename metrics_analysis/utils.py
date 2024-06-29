from django.db.models import Count, Sum
from django.db.models.functions import  TruncMonth
from barter.models import Barter
from branches.models import Branch
from posts.models import Post
from posts.models import PackagePurchase, Package


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


def cut_address(address):
    index = address.find(" - CP")
    if index != -1:
        return address[:index]
    else:
        return address


class BarterCharts:
    def info_chart_1(self, year):
        """Number of barters per month"""
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

    def number_finished_barters(self, year):
        """Number of finished barters per branch."""
        barter_branch_count = list(
            Barter.objects.filter(finished_date__year=year)
            .values("branch")
            .annotate(count=Count("id"))
        )

        labels = []
        data = []
        for branch_count in barter_branch_count:
            branch = branch_count["branch"]
            if branch is not None:
                branch_obj = Branch.objects.get(id=branch)
                branch_name = cut_address(str(branch_obj))
                labels.append(branch_name)
            else:
                labels.append("No branch")
            data.append(branch_count["count"])

        return labels, data

    def info_chart_2(self):
        """Number of barters by state."""
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
        """Number of barters per branch."""
        barter_branch_count = list(
            Barter.objects.values("branch").annotate(count=Count("id"))
        )

        labels = []
        data = []
        for branch_count in barter_branch_count:
            branch = branch_count["branch"]
            if branch is not None:
                branch_obj = Branch.objects.get(id=branch)
                branch_name = cut_address(str(branch_obj))
                labels.append(branch_name)
            else:
                labels.append("No branch")
            data.append(branch_count["count"])

        return labels, data
    # Barter.objects.filter(state="committed")
    def info_chart_5(self):
        """Number of barters per category"""
        barter_requesting_post_count = list(
            Barter.objects.values("requested_post")
        )
        labels=[]
        data=[]
        CATEGORY_NAMES = {
           "tools": "Herramientas",
           "construction": "Construcción",
           "general_hardware_store": "Ferretería general",
           "electrical": "Electricidad",
           "plumbing": "Fontanería",
           "gardens": "Jardin",
        }

        category_counter = {
            "tools": 0,
            "construction": 0,
            "general_hardware_store": 0,
            "electrical": 0,
            "plumbing": 0,
            "gardens": 0,
        }
        for post_count in barter_requesting_post_count:
            requested_post = post_count["requested_post"]
            requested_post_obj = Post.objects.get(id=requested_post)
            requested_post_category = requested_post_obj.category
            category_counter[requested_post_category]+=1

        for key in category_counter:
            if (category_counter[key] > 0):
                labels.append(CATEGORY_NAMES[key])
                data.append(category_counter[key])

        # data.append(post_count["count"])

        return labels, data

    def info_chart_6(self, year):
        """Number of commited barters per category in a particular year"""
        barter_requesting_post_count = list(
            Barter.objects.filter(finished_date__year=year)
            .values("requested_post")
        )
        labels=[]
        data=[]
        CATEGORY_NAMES = {
           "tools": "Herramientas",
           "construction": "Construcción",
           "general_hardware_store": "Ferretería general",
           "electrical": "Electricidad",
           "plumbing": "Fontanería",
           "gardens": "Jardin",
        }

        category_counter = {
            "tools": 0,
            "construction": 0,
            "general_hardware_store": 0,
            "electrical": 0,
            "plumbing": 0,
            "gardens": 0,
        }
        for post_count in barter_requesting_post_count:
            requested_post = post_count["requested_post"]
            requested_post_obj = Post.objects.get(id=requested_post)
            requested_post_category = requested_post_obj.category
            category_counter[requested_post_category]+=1

        for key in category_counter:
            if (category_counter[key] > 0):
                labels.append(CATEGORY_NAMES[key])
                data.append(category_counter[key])

        # data.append(post_count["count"])

        return labels, data


class IncomeCharts:
    def barter_income_per_month(self, year):
        """Income per month"""
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

    def barter_income_per_branch(self, year):
        """Income per branche"""
        income_per_branch = list(
            Barter.objects.filter(finished_date__year=year)
            .values("branch")
            .annotate(total_income=Sum("income"))
            .values("branch", "total_income")
        )

        labels = []
        data = []
        for income in income_per_branch:
            branch = income["branch"]
            if branch is not None:
                branch_obj = Branch.objects.get(id=branch)
                branch_name = cut_address(str(branch_obj))
                labels.append(branch_name)
            else:
                labels.append("No branch")
            data.append(
                float(income["total_income"]) if income["total_income"] else 0.0
            )

        return labels, data

    def package_income_per_month(self, year):
        """Income per month"""
        values = [0] * 12
        package_per_month = list(
            PackagePurchase.objects.filter(purchase_date__year=year)
            .annotate(month=TruncMonth("purchase_date"))
            .values("month")
            .annotate(total_income=Sum("price"))
            .order_by("month")
            .values("month", "total_income")
        )

        # Preparar los datos para el gráfico
        for package in package_per_month:
            month = package["month"].month - 1  # Subtract 1 to convert to 0-indexed
            values[month] = (
                float(package["total_income"]) if package["total_income"] else 0.0
            )

        return MONTHS_NAMES, values

    def income_per_package(self, year):
        """Income per package"""
        income_per_package = list(
            PackagePurchase.objects.filter(purchase_date__year=year)
            .values("package")
            .annotate(total_income=Sum("price"))
            .values("package", "total_income")
        )

        labels = []
        data = []
        for income in income_per_package:
            package = income["package"]
            if package is not None:
                package_obj = Package.objects.get(id=package)
                labels.append(str(package_obj))
            else:
                labels.append("No package")
            data.append(
                float(income["total_income"]) if income["total_income"] else 0.0
            )

        return labels, data
