from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .models import Order, OrderPizza, OrderSub, OrderPasta, OrderSalad, OrderDinnerPlatter, Topping, Size, PizzaName, Pizza, SubName, Sub, SubAddon, Pasta, Salad, DinnerPlatterName, DinnerPlatter


def index(request):
    context = {
        "pizzas": PizzaName.objects.all(),
        "subs": SubName.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "dinner_platters": DinnerPlatterName.objects.all()
    }
    return render(request, "orders/index.html", context=context)


def register_view(request):
    if request.method == "GET":
        return render(request, "orders/register.html")

    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken', extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('register'))

        else: 
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            messages.success(request, 'You are now registered', extra_tags='alert-success')
            return HttpResponseRedirect(reverse('login'))


def login_view(request):
    if request.method == "GET":
        return render(request, "orders/login.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, 'You entered the wrong username or password', extra_tags='alert-danger')
            return HttpResponseRedirect(reverse("login"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def add_to_cart(request):
    if request.method == "GET":
        return HttpResponseNotAllowed()

    order = Order.objects.filter(user__pk=request.user.id).filter(order_sent=False)
    if order.count() == 0:
        order = Order(user=request.user)
        order.save()
    else:
        order = order[0]

    # Get product data
    try:
        product_class = request.POST["product_class"]
        product_name = request.POST["product_name"]
        product_id = int(request.POST["product_id"])
    except (KeyError, ValueError):
        return HttpResponseBadRequest()

    # Get other request parameters
    quantity = int(request.POST["quantity"])

    # Add to order
    if product_class == "DinnerPlatterName":
        order_dinner_platter = OrderDinnerPlatter(
            order=order,
            dinner_platter=DinnerPlatter.objects.get(
                name=DinnerPlatterName.objects.get(name=product_name),
                size=Size.objects.get(pk=int(request.POST["size"]))
            ),
            quantity=quantity
        )
        order_dinner_platter.save()
        order.save()
    elif product_class == "Salad":
        order_salad = OrderSalad(
            order=order,
            salad=Salad.objects.get(
                name=Salad.objects.get(name=product_name)
            ),
            quantity=quantity
        )
        order_salad.save()
        order.save()
    elif product_class == "Pasta":
        order_pasta = OrderPasta(
            order=order,
            pasta=Pasta.objects.get(
                name=Pasta.objects.get(name=product_name)
            ),
            quantity=quantity
        )
        order_pasta.save()
        order.save()
    elif product_class == "Sub":
        order_sub = OrderSub(
            order=order,
            sub=Sub.objects.get(
                name=SubName.objects.get(name=product_name),
                size=Size.objects.get(pk=int(request.POST["size"]))
            ),
            quantity=quantity
        )
        order_sub.save()
        for addon_id in request.POST.get("subaddons", []).split(","):
            order_sub.sub_addons.add(
                SubAddon.objects.get(pk=int(addon_id))
            )
        order_sub.save()

        order.save()
    elif product_class == "PizzaName":
        order_pizza = OrderPizza(
            order=order,
            pizza=Pizza.objects.get(
                name=PizzaName.objects.get(name=product_name),
                size=Size.objects.get(pk=int(request.POST["size"])),
                toppings_count=int(request.POST["toppings_count"])
            ),
            quantity=quantity
        )
        order_pizza.save()
        for topping_id in request.POST.get("toppings", []).split(","):
            order_pizza.toppings.add(
                Topping.objects.get(pk=int(topping_id))
            )
        order_pizza.save()

        order.save()
    else:
        return HttpResponseNotFound()


    return JsonResponse({
        "order_price": order.get_order_price(),
        "order_id": order.id
    })


@csrf_exempt
def remove_from_cart(request):
    if request.method == "GET":
        return HttpResponseNotAllowed()

    order_class = request.POST["order_class"]
    order_id = request.POST["order_id"]

    order = Order.objects.filter(user__pk=request.user.id).filter(order_sent=False)[0]

    class_obj = globals()[order_class]
    order_product = class_obj.objects.get(pk=order_id)
    order_product.delete(keep_parents=True)

    return JsonResponse({
        "order_price": order.get_order_price(),
        "order_id": order.id
    })


@csrf_exempt
def get_sizes(request):
    if request.method == "GET":
        return HttpResponseNotAllowed()

    product_class = request.POST["product_class"]
    product_id = request.POST["product_id"]

    if product_class == "DinnerPlatterName":
        objects = DinnerPlatter.objects.filter(name__pk=product_id)
        sizes = [{"size_name": x.size.name, "size_value": x.size.pk} for x in objects]
    elif product_class == "Sub":
        objects = Sub.objects.filter(name__pk=product_id)
        sizes = [{"size_name": x.size.name, "size_value": x.size.pk} for x in objects]
    elif product_class == "PizzaName":
        objects = Pizza.objects.filter(name__pk=product_id)
        sizes_ids = set([x.size.id for x in objects])
        sizes = [{"size_name": Size.objects.get(pk=x).name, "size_value": x} for x in sizes_ids]
    else:
        return HttpResponseNotFound()

    if sizes:
        return JsonResponse(sizes, safe=False)
    else:
        return HttpResponseNotFound()


@csrf_exempt
def get_subs_addons(request):
    if request.method == "GET":
        return HttpResponseNotAllowed()

    addons_all = SubAddon.objects.all()
    addons = []
    if addons_all.count() > 0:
        addons = [{"subaddon_name": x.name, "subaddon_value": x.pk} for x in addons_all]

    return JsonResponse(addons, safe=False)


@csrf_exempt
def get_toppings(request):
    if request.method == "GET":
        return HttpResponseNotAllowed()

    toppings_all = Topping.objects.all()
    toppings = []
    if toppings_all.count() > 0:
        toppings = [{"topping_name": x.name, "topping_value": x.pk} for x in toppings_all]

    return JsonResponse(toppings, safe=False)


@csrf_exempt
def get_toppings_count(request):
    if request.method == "GET":
        return HttpResponseNotAllowed()

    product_id = request.POST["product_id"]

    toppings_counts_all = Pizza.objects.filter(
        name=PizzaName.objects.get(pk=product_id)
    ).all()
    toppings = []
    if toppings_counts_all.count() > 0:
        toppings = list(set([x.toppings_count for x in toppings_counts_all]))

    return JsonResponse(toppings, safe=False)


@csrf_exempt
def get_current_order_price(request):
    if request.method == "GET":
        return HttpResponseNotAllowed()

    order_price = 0
    order_id = None
    order = Order.objects.filter(user__pk=request.user.id).filter(order_sent=False)
    if order.count() > 0:
        order = order[0]
        order_price = order.get_order_price()
        order_id = order.id

    return JsonResponse({"order_price": order_price, "order_id": order_id}, safe=False)


@csrf_exempt
def confirm_order_final(request):
    if request.method == "POST":
        order = Order.objects.filter(user__pk=request.user.id).filter(order_sent=False)
        if order.count() == 0:
            return HttpResponseNotFound()
        else:
            order = order[0]

        order.order_sent = True
        order.save()

        return JsonResponse({"success": True}, safe=False)
    else:
        return HttpResponseNotAllowed()


@csrf_exempt
def cancel_order(request):
    if request.method == "GET":
        return HttpResponseNotAllowed()

    order = Order.objects.filter(user__pk=request.user.id).filter(order_sent=False)
    if order.count() == 0:
        return HttpResponseNotFound()
    else:
        order = order[0]

    order.delete(keep_parents=True)

    return JsonResponse({"success": True}, safe=False)


@login_required
def order(request, order_id=None):
    context = {
        "order_exists": False
    }

    if order_id is None:
        order = Order.objects.filter(user__pk=request.user.id).filter(order_sent=False)
        if order.count() == 0:
            return render(request, "orders/order.html", context=context)
        else:
            order = order[0]
    else:
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotFound:
            return render(request, "orders/order.html", context=context)

    context["order_exists"] = True
    context.update({
        "pizzas": OrderPizza.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "subs": OrderSub.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "pastas": OrderPasta.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "salads": OrderSalad.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "dinner_platters": OrderDinnerPlatter.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "overall_price": order.get_order_price()
    })

    if order_id is None:
        context["order_title"] = "Your current order"
        context["buttons"] = True
    else:
        context["order_title"] = f"Order #{order_id}"
        context["buttons"] = False

    return render(request, "orders/order.html", context=context)


@login_required
def account(request):
    context = {
        "orders": []
    }

    orders = Order.objects.filter(user__pk=request.user.id).filter(order_sent=True).order_by("-created")
    context["orders"] = orders

    return render(request, "orders/account.html", context=context)
