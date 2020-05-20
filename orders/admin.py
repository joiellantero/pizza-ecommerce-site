from django.contrib import admin

from .models import Size, Topping, SubAddon, PizzaName, Pizza, SubName, Sub, Pasta, Salad, DinnerPlatterName, DinnerPlatter, Order


class SizeAdmin(admin.ModelAdmin):
    pass


class ToppingAdmin(admin.ModelAdmin):
    pass


class SubAddonAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


class PizzaNameAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "description")


class PizzaAdmin(admin.ModelAdmin):
    list_display = ("name", "size", "toppings_count", "price")


class SubNameAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "description")


class SubAdmin(admin.ModelAdmin):
    list_display = ("name", "size", "price")


class PastaAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "description", "price")


class SaladAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "description", "price")


class DinnerPlatterNameAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "description")


class DinnerPlatterAdmin(admin.ModelAdmin):
    list_display = ("name", "size", "price")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "order_sent", "order_completed", "_get_pizzas_list", "_get_subs_list", "_get_pastas_list", "_get_salads_list", "_get_dinner_platters_list", "_get_order_price")
    readonly_fields = ("_get_pizzas_list", "_get_subs_list", "_get_pastas_list", "_get_salads_list", "_get_dinner_platters_list", "_get_order_price")

    def _get_pizzas_list(self, obj):
        return obj.get_pizzas_list()
    _get_pizzas_list.short_description = 'Pizzas'

    def _get_subs_list(self, obj):
        return obj.get_subs_list()
    _get_subs_list.short_description = 'Subs'

    def _get_pastas_list(self, obj):
        return obj.get_pastas_list()
    _get_pastas_list.short_description = 'Pastas'

    def _get_salads_list(self, obj):
        return obj.get_salads_list()
    _get_salads_list.short_description = 'Salads'

    def _get_dinner_platters_list(self, obj):
        return obj.get_dinner_platters_list()
    _get_dinner_platters_list.short_description = 'Dinner Platters'

    def _get_order_price(self, obj):
        return obj.get_order_price()
    _get_order_price.short_description = 'Order Price'


admin.site.register(Size, SizeAdmin)
admin.site.register(Topping, ToppingAdmin)
admin.site.register(SubAddon, SubAddonAdmin)
admin.site.register(PizzaName, PizzaNameAdmin)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(SubName, SubNameAdmin)
admin.site.register(Sub, SubAdmin)
admin.site.register(Pasta, PastaAdmin)
admin.site.register(Salad, SaladAdmin)
admin.site.register(DinnerPlatterName, DinnerPlatterNameAdmin)
admin.site.register(DinnerPlatter, DinnerPlatterAdmin)
admin.site.register(Order, OrderAdmin)
