from django.conf.urls import url
from django.contrib import admin

from inventory.views import AddItemView, ItemListView

urlpatterns = [
    url(r'^add/$', AddItemView.as_view(), name='add_item'),
    url(r'^items/$', ItemListView.as_view(), name='items'),
]