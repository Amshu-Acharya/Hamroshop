from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.serializer import CategorySerializer
from .models import Menu, Category, Banner, Product, Cart
from .forms import ReviewForm


class BaseView(View):
    template_context = {
        'menus': Menu.objects.order_by('-Weight'),
        'categories': Category.objects.all(),
    }


class HomeView(BaseView):
    def get(self, request):
        context = {
            'banners': Banner.objects.all(),
            'deals_of_the_day': Product.objects.filter(deal_of_day=True),  # database ma query banaucha.
            'latest_products': Product.objects.order_by('-pub_date')[:5],
            'random_products': Product.objects.order_by('?')[:4]
        }
        context.update(self.template_context)
        return render(request, 'index.html', context)


class ProductView(BaseView):
    def get(self, request, product_slug):
        return self.some_part(request, product_slug, ReviewForm())

    def post(self, request, product_slug):
        print(request.POST)
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(comit=False)
            review.user = request.user
            review.product = Product.objects.get(slug=product_slug)
            review.save()

            return redirect('product_page', product_slug)

        else:
            return self.some_part(request, product_slug, form)

    def some_part(self, request, product_slug, form):

        product = Product.objects.get(slug=product_slug)

        context = {

            'product': product,
            'random_products': Product.objects.order_by('?')[:4],
            'form': form

        }
        context.update(self.template_context)
        return render(request, 'product.html', context)


class SignUpView(BaseView):
    def get(self, request):
        form = UserCreationForm()

        context = {
            'form': form
        }
        context.update(self.template_context)
        return render(request, 'registration/register.html', context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

        else:
            context = {
                'form': form
            }
            context.update(self.template_context)
            return render(request, 'registration/register.html', context)


class CartView(BaseView, LoginRequiredMixin):
    def Post(self, request, product_slug):
        qty = request.POST.get('qty', 1)
        cart_item = Cart()
        cart_item.qty = qty
        cart_item.user = request.user
        cart_item.product = Product.objects.get(slug=product_slug)
        cart_item .save()
        return redirect('product_page',product_slug)


class CategoryList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)