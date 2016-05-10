import logging

from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

# Create your views here.
class AddItemView(TemplateView):
    """docstring for AddItemView"""
    
    template_name = 'inventory/add_item.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            return super(AddItemView, self).dispatch(request, *args, **kwargs)
        except Exception, e:
            logger.error("%s: %s" % (e.__class__.__name__, e))
    
    
class ItemListView(TemplateView):
    """docstring for ItemListView"""
    
    template_name = 'inventory/items.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            return super(ItemListView, self).dispatch(request, *args, **kwargs)
        except Exception, e:
            logger.error("%s: %s" % (e.__class__.__name__, e))
        