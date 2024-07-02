# Python
from typing import Dict, Optional
# Django
from django.views.generic import View, ListView, UpdateView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.http import (
     JsonResponse,
     HttpResponseBadRequest,
     HttpResponseServerError,
     HttpResponseNotFound
)
# Local
from .models import Product
from .services import (
    get_active_products,
    get_product_by_code,
    filter_products_by_query_params,
    get_product_images,
    delete_product_by_code,
    toggle_product_visibility, get_hidden_products
)
from .forms import ProductCreationForm, ProductImageCreationForm
from accounts.mixins import AdminRequiredMixin


class ProductListView(ListView):
    model = Product
    context_object_name = "product_list"
    template_name = "product_list.html"

    def get_queryset(self):
        return get_active_products()


class ProductSearchView(ListView):
    model = Product
    context_object_name = "product_list"
    template_name = "product_list.html"

    def get_queryset(self):
        query_params = self._get_query_params()
        return filter_products_by_query_params(query_params)

    def _get_query_params(self) -> Dict:
        name_query = self.request.GET.get("name")
        raw_categories_query = self.request.GET.get("categories")

        if raw_categories_query:
            categories_query = raw_categories_query.split(",")
        else:
            categories_query = ""
        
        min_price = self._extract_float(self.request.GET.get("min_price"))
        max_price = self._extract_float(self.request.GET.get("max_price"))

        return {
            "name": name_query,
            "categories": categories_query,
            "prices": {
                "min_price": min_price,
                "max_price": max_price
            }
        }
    
    @staticmethod
    def _extract_float(str_value: str) -> Optional[float]:
        try:
            converted_value = float(str_value)
        except ValueError:
            return None
        except Exception as e:
            print(e)
            return None
        return converted_value


class ProductCreateView(AdminRequiredMixin, View):
    
    template_name = "product_creation.html"

    def get(self, request, *args, **kwargs):
        creation_form = ProductCreationForm()
        image_form = ProductImageCreationForm()
        context = {
            "product_form": creation_form,
            "image_form": image_form
        }
        return render(
            request,
            template_name="product_create.html",
            context=context
        )

    def post(self, request, *args, **kwargs):
        try:
            form = ProductCreationForm(request.POST, request.FILES)
            if form.is_valid():
                new_product = form.save()
                response = JsonResponse({
                    "product_code": new_product.code,
                    "product_id": new_product.id
                })
                response.status_code = 200
            else:
                response = JsonResponse({
                    "errors": form.errors.as_json()
                })
                response.status_code = 400
            return response
        except Exception as e:
            print(e)
            return HttpResponseServerError()


class ProductImageUploadView(View, AdminRequiredMixin):
    
    def post(self, request, *args, **kwargs):
        try:
            form = ProductImageCreationForm(request.POST, request.FILES)
            if form.is_valid():
                new_image = form.save()
                response = JsonResponse({
                    "id": new_image.id,
                    "product": new_image.product.code,
                    "image": new_image.image.url,
                    "title": new_image.title
                })
                response.status_code = 200
            else:
                response = HttpResponseBadRequest()
            return response
        except Exception as e:
            print(e)
            return HttpResponseServerError()


class ProductDetailView(View):
    template_name = "product_detail.html"

    def get(self, request, *args, **kwargs):
        try:
            code = kwargs.get("code")
            product = get_product_by_code(code)
            if product is not None:
                images = get_product_images(product)
                context = {
                    "product": product,
                    "product_images": images
                }
                return render(
                    request,
                    template_name="product_detail.html",
                    context=context
                )
            else:
                return HttpResponseNotFound()
        except Exception as e:
            print(e)
            return HttpResponseServerError()


class ProductDeleteView(View, AdminRequiredMixin):

    def post(self, request, *args, **kwargs):
        try:
            code = kwargs.get("code")
            result = delete_product_by_code(code)
            if result:
                return redirect("product_delete_success")
            else:
                return HttpResponseNotFound()
        except Exception as e:
            print(e)
            return HttpResponseServerError()


class ProductDeleteSuccessMessageView(View, AdminRequiredMixin):
    def get(self, request, *args, **kwargs):
        return render(request, "messages/product_delete_success.html")


class ProductVisibilityToggleView(View, AdminRequiredMixin):
    def post(self, request, *args, **kwargs):
        try:
            code = kwargs.get("code")
            success = toggle_product_visibility(code)
            if success:
                return redirect("product_visibility_change_success")
            else:
                return HttpResponseNotFound()
        except Exception as e:
            print(e)
            return HttpResponseServerError()


class ProductVisibilityChangeSuccessMessageView(View, AdminRequiredMixin):
    def get(self, request, *args, **kwargs):
        return render(request, "messages/product_visibility_change_success.html")


class HiddenProductListView(ListView):
    model = Product
    context_object_name = "product_list"
    template_name = "hidden_product_list.html"

    def get_queryset(self):
        return get_hidden_products()


class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "brand", "description", "model", "category", "stock", "price"]
    template_name = "product_edit.html"

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'code': self.object.code})
