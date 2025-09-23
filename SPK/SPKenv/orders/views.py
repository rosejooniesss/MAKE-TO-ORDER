from django.shortcuts import render, redirect
from .forms import OrderForm, OrderItemForm, OrderItemFormSet
from .models import Order

def home(request):
    return render(request, "orders/home.html")

def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save()
            items = formset.save(commit=False)
            for item in items:
                item.order = order
                item.save()
            return redirect('orders:list')
    else:
        order_form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, 'orders/order_form.html', {
        'order_form': order_form,
        'formset': formset
    })


def order_success(request):
    return render(request, "orders/order_success.html")