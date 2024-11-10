from itertools import product

from products.models import Product, ProductCategory
from django.shortcuts import render

def index(request):
    context = {
        'title' : 'Store',
    }
    return render(request, 'products./index.html', context)

def products(request):
    context = {
        'title' : 'Store - Каталог',
        'products' : Product.objects.all(), # Он заходит в бд и извлекает из него все объекты и передает в шаблон
        'categories' : ProductCategory.objects.all(),
    }
    return render(request, 'products./products.html', context)
