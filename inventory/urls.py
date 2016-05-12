from django.conf.urls import url
from django.contrib import admin

from inventory.views import AddItemView, ItemListView, ajax_checkout_item, ajax_checkin_item

urlpatterns = [
    url(r'^checkin/(?P<record_id>\d+)/', ajax_checkin_item, name='checkin'),
    url(r'^checkout/', ajax_checkout_item, name='checkout'),
    url(r'^add/$', AddItemView.as_view(), name='add_item'),
    url(r'^items/$', ItemListView.as_view(), name='items'),
]