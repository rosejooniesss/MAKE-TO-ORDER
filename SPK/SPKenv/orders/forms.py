from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem, Product

# Form for the Order itself
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name']  # changed from 'customer' to 'customer_name'
        widgets = {
            'customer_name': forms.TextInput(attrs={'placeholder': 'Enter customer name'}),
        }
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(),
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }
# Form for each OrderItem
OrderItemFormSet = inlineformset_factory(
    Order, OrderItem,
    form=OrderItemForm,
    extra=1,  # start with 1 row
    can_delete=True  # allows removing items
)