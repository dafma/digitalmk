from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from digitalmarkey.mixins import (
        LoginRequiredMixin,
        MultiSlugMixin,
        SubmitBtnMixin
        )
from .mixins import ProductManagerMixin
from .models import Product
from .forms import ProductAddForm, ProductModelForm


class ProductCreateView(LoginRequiredMixin,SubmitBtnMixin, CreateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    success_url = "/products/add/"
    submit_btn = "Add Product"
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        valid_data = super(ProductCreateView, self).form_valid(form)
        form.instance.managers.add(user)
        return valid_data


class ProductUpdateView(ProductManagerMixin,SubmitBtnMixin, MultiSlugMixin, UpdateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    success_url = "/product/"
    submit_btn = "Add Update"

    # def get_object(self, *args, **kwargs):
    #     user = self.request.user
    #     obj = super(ProductUpdateView, self).get_object(*args, **kwargs)
    #     if obj.user == user or user in obj.managers.all():
    #         return  obj
    #     else:
    #         raise Http404


class ProductDetailView(MultiSlugMixin, DetailView):
    model = Product

# def get_object(self, *args, **kwargs):
# 	slug = self.kwargs.get("slug")
# 	ModelClass = self.model
# 	if slug is not None:
# 		try:
# 			product = get_object_or_404(ModelClass, slug=slug)
# 		except ModelClass.MultipleObjectsReturned:
# 			product = ModelClass.objects.filter(slug=slug).order_by("-title").first()
# 	else:
# 		obj = super(ProductDetailView, self).get_object(*args, **kwargs)
# 		return obj


class ProductListView(ListView):
    model = Product
    # template_name = "list_view.html"

    # def get_context_data(self, **kwargs):
    # context = super(ProductListView, self).get_context_data(**kwargs)
    # context["queryset"] = Product.objects.all()
    # return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(**kwargs)
        # qs = qs.filter(title__icontains="aaaa")
        return qs


def create_view(request):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.sale_price = instance.price
        instance.save()
    # form = ProductAddForm(request.POST or None)
    # if form.is_valid():
    # data = form.cleaned_data
    # title = data.get("title")
    # description = data.get("description")
    # price = data.get("price")
    # new_obj = Product.objects.create(title=title, description=description, price=price)
    template = "create_view.html"
    context = {
        "form": form,
    }
    return render(request, template, context)


def update_view(request, object_id=None):
    product = get_object_or_404(Product, id=object_id)
    form = ProductModelForm(request.POST or None, instance=product)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    template = "form.html"
    context = {
        "object": product,
        "form": form,
        "submit_btn": "Update Product"
    }
    return render(request, template, context)


# Create your views here.
def detail_slug_view(request, slug=None):
    try:
        product = get_object_or_404(Product, slug=slug)
    except Product.MultipleObjectsReturned:
        product = Product.objects.filter(slug=slug).order_by("-title").first()
    template = 'detail_view.html'
    context = {
        "object": product,
    }
    return render(request, template, context)


def detail_view(request, object_id=None):
    product = get_object_or_404(Product, id=object_id)
    template = 'detail_view.html'
    context = {
        "object": product,
    }
    return render(request, template, context)


def list_view(request):
    queryset = Product.objects.all()
    template = 'list_view.html'
    context = {
        "queryset": queryset,
    }
    return render(request, template, context)
