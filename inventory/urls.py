from django.conf.urls import url
from django.contrib import admin

from inventory.views import (
    AddItemView,
    ItemListView,
    ajax_checkout_item,
    ajax_checkin_item,
    ajax_useup_item,
    ajax_get_items_by_category_html,
    ajax_get_items_by_category,
    ajax_get_list_html,
    ajax_get_list_items_out_json,
    ajax_get_list_items_out_html,
    ajax_get_records_by_item_html)

urlpatterns = [
    url(r'^checkin/(?P<record_id>\d+)/', ajax_checkin_item, name='checkin'),
    url(r'^useup/(?P<record_id>\d+)/', ajax_useup_item, name='useup'),
    url(r'^checkout/', ajax_checkout_item, name='checkout'),
    url(r'^add/$', AddItemView.as_view(), name='add_item'),
    url(r'^items/$', ItemListView.as_view(), name='items'),
    url(r'^ajax_get_items_by_category/', ajax_get_items_by_category, name="ajax_get_items_by_category"),
    url(r'^ajax_get_items_by_category_html/', ajax_get_items_by_category_html, name="ajax_get_items_by_category_html"),
    url(r'^ajax_get_list_html/', ajax_get_list_html, name="ajax_get_list_html"),
    url(r'^ajax_get_list_items_out_json', ajax_get_list_items_out_json, name="ajax_get_list_items_out_json"),
    url(r'^ajax_get_list_items_out_html', ajax_get_list_items_out_html, name="ajax_get_list_items_out_html"),
    url(r'^ajax_get_records_by_item_html/', ajax_get_records_by_item_html, name="ajax_get_records_by_item_html"),
]