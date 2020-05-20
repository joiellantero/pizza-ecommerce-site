from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


# Product variables
class Size(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class SubAddon(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal("0.0"))

    def __str__(self):
        return self.name


# Products
class PizzaName(models.Model):
    name = models.CharField(max_length=32)
    image = models.ImageField(default="placeholder.jpg")
    description = models.TextField(default="")

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.ForeignKey(PizzaName, on_delete=models.CASCADE, related_name="pizzas")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="pizzas")
    toppings_count = models.PositiveSmallIntegerField(default=0)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal("0.0"))

    def __str__(self):
        return self.name.__str__()


class SubName(models.Model):
    name = models.CharField(max_length=32)
    image = models.ImageField(default="placeholder.jpg")
    description = models.TextField(default="")

    def __str__(self):
        return self.name


class Sub(models.Model):
    name = models.ForeignKey(SubName, on_delete=models.CASCADE, related_name="subs")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="subs")
    price = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal("0.0"))

    def __str__(self):
        return self.name.name


class Pasta(models.Model):
    name = models.CharField(max_length=32)
    image = models.ImageField(default="placeholder.jpg")
    description = models.TextField(default="")
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name


class Salad(models.Model):
    name = models.CharField(max_length=32)
    image = models.ImageField(default="placeholder.jpg")
    description = models.TextField(default="")
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name


class DinnerPlatterName(models.Model):
    name = models.CharField(max_length=32)
    image = models.ImageField(default="placeholder.jpg")
    description = models.TextField(default="")

    def __str__(self):
        return self.name


class DinnerPlatter(models.Model):
    name = models.ForeignKey(DinnerPlatterName, on_delete=models.CASCADE, related_name="dinner_platters")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="dinner_platters")
    price = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.0'))

    def __str__(self):
        return self.name.__str__()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created = models.DateTimeField(auto_now_add=True)
    order_sent = models.BooleanField(default=False)
    order_completed = models.BooleanField(default=False)
    pizzas = models.ManyToManyField(Pizza, through="OrderPizza")
    subs = models.ManyToManyField(Sub, blank=True, through="OrderSub")
    pastas = models.ManyToManyField(Pasta, blank=True, through="OrderPasta")
    salads = models.ManyToManyField(Salad, blank=True, through="OrderSalad")
    dinner_platters = models.ManyToManyField(DinnerPlatter, blank=True, through="OrderDinnerPlatter")

    def get_pizzas_list(self):
        return ", ".join([f"{x.name.name}" for x in self.pizzas.all()])

    def get_subs_list(self):
        return ", ".join([f"{x.name.name}" for x in self.subs.all()])

    def get_pastas_list(self):
        return ", ".join([f"{x.name}" for x in self.pastas.all()])

    def get_salads_list(self):
        return ", ".join([f"{x.name}" for x in self.salads.all()])

    def get_dinner_platters_list(self):
        return ", ".join([f"{x.name.name} ({x.size.name})" for x in self.dinner_platters.all()])


    def get_order_price(self):
        price = 0

        # Pizzas
        price += sum([x.get_price() * x.quantity for x in OrderPizza.objects.filter(order__id=self.id)])

        # Subs
        price += sum([x.get_price() * x.quantity for x in OrderSub.objects.filter(order__id=self.id)])

        # Pastas
        price += sum([x.get_price() * x.quantity for x in OrderPasta.objects.filter(order__id=self.id)])

        # Salads
        price += sum([x.get_price() * x.quantity for x in OrderSalad.objects.filter(order__id=self.id)])

        # Dinner Platters
        price += sum([x.get_price() * x.quantity for x in OrderDinnerPlatter.objects.filter(order__id=self.id)])

        return price

    def __str__(self):
        return self.user.__str__()


class OrderPizza(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping)
    quantity = models.PositiveIntegerField()

    def get_price(self):
        return self.pizza.price

    def get_toppings(self):
        return ", ".join([x.name for x in self.toppings.all()])


class OrderSub(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE)
    sub_addons = models.ManyToManyField(SubAddon, blank=True)
    quantity = models.PositiveIntegerField()

    def get_price(self):
        price = self.sub.price
        if self.sub_addons.count() > 0:
            price += sum([x.price for x in self.sub_addons.all()])
        price *= self.quantity
        return price

    def get_addons(self):
        return ", ".join([x.name for x in self.sub_addons.all()])


class OrderPasta(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pasta = models.ForeignKey(Pasta, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_price(self):
        return self.pasta.price * self.quantity


class OrderSalad(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    salad = models.ForeignKey(Salad, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_price(self):
        return self.salad.price * self.quantity


class OrderDinnerPlatter(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dinner_platter = models.ForeignKey(DinnerPlatter, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_price(self):
        return self.dinner_platter.price * self.quantity
