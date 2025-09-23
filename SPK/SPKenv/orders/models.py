from django.db import models

# Customer model (optional if you want to store email info)
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

# Product model
class Product(models.Model):
    sku = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # PHP

    def __str__(self):
        return f"{self.sku} - {self.name} (₱{self.price})"

# Order model
class Order(models.Model):
    customer_name = models.CharField(max_length=255)  # free text input
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

# OrderItem model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
