from django import forms
from .models import OrderItem, Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer']  # just pick customer for now

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
