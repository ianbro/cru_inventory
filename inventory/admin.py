from django.contrib import admin

from inventory.models import Item, ItemRecord, Category

# Register your models here.
admin.site.register(Item)
admin.site.register(ItemRecord)
admin.site.register(Category)