from django.contrib import admin
from crust.items.models import Item
from crust.items.models import Meal
from crust.items.models import Recipe

admin.site.register(Item)
admin.site.register(Meal)
admin.site.register(Recipe)


