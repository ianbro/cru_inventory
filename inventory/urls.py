from django.conf.urls import url
from django.contrib import admin

from inventory.views import AddItemView, ItemListView, ajax_checkout_item

urlpatterns = [
    url(r'^checkout/(?P<item_id>\d+)/', ajax_checkout_item, name='checkout'),
    url(r'^add/$', AddItemView.as_view(), name='add_item'),
    url(r'^items/$', ItemListView.as_view(), name='items'),
]