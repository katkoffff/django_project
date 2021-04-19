from django.shortcuts import render
from django.views.generic import View, ListView, UpdateView, CreateView, DetailView, DeleteView
from .models import Product, Category
import datetime
from django.core.paginator import Paginator
from .filters import ProductFilter
from .forms import ProductForm


class Products(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 5


class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    context_object_name = 'product_detail'
    queryset=Product.objects.all()


class ProductCreateView(CreateView):
    template_name = 'product_create.html'
    context_object_name = 'product_create'
    form_class = ProductForm
    success_url = '/products/'

class ProductUpdateView(UpdateView):
    template_name = 'product_update.html'
    context_object_name = 'product_update'
    form_class = ProductForm
    success_url = '/products/'
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Product.objects.get(pk=id)


class ProductDeleteView(DeleteView):
    template_name = 'product_delete.html'
    context_object_name = 'product_delete'
    queryset = Product.objects.all()
    success_url = '/products/'