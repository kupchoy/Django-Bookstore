import stripe
from django.conf import settings
from django.contrib.auth.models import Permission
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from .models import Cart
from books.models import Book

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class CartPageView(TemplateView):
    template_name = 'carts/cart_main.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_key'] = settings.STRIPE_TEST_PUBLISHABLE_KEY
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context.update({'cart': cart_obj})
        return context


def cart_update(request):
    book_id = request.POST.get('book_id')
    if book_id is not None:
        try:
            book_obj = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return redirect('cart')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if book_obj in cart_obj.books.all():
            cart_obj.books.remove(book_obj)
        else:
            cart_obj.books.add(book_obj)
    request.session['cart_items'] = cart_obj.books.count()
    return redirect('cart')


def purchase(request):
    permission = Permission.objects.get(codename='special_status')
    u = request.user
    u.user_permissions.add(permission)

    total = request.POST.get('total')
    total = int(float(total) * 100)
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=total,
            currency='usd',
            description='Purchase books',
            source=request.POST['stripeToken']
        )
        request.session['cart_items'] = 0
        del request.session['cart_id']
    return redirect('success')


class SuccessPageView(TemplateView):
    template_name = 'carts/success.html'


def cart_home(request):
    cart_obj = Cart.objects.new_or_get(request)
    return render(request, 'carts/cart_main.html', {'cart': cart_obj})