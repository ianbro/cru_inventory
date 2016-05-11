import logging

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from inventory.models import Item, ItemRecord
from inventory.forms import CreateItemForm

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
            raise e
            
    def get_context_data(self, *args, **kwargs):
        context = super(AddItemView, self).get_context_data(*args, **kwargs)
        context['form'] = CreateItemForm(self.request.POST or None)
        return context
        
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        if context['form'].is_valid():
            context['form'].save()
            return HttpResponseRedirect(reverse('inv:items'))
        else:
            return render(request, self.template_name, context)
            
            
def ajax_checkout_item(request, item_id, *args, **kwargs):
    json_data = {}
    
    user = request.user
    amount = int(request.GET['amount'])
    
    try:
        item_record = Item.objects.get(id=item_id).checkout(user, amount)
        json_data.update({
            "person": "%s %s" % (item_record.person.first_name,
                                    item_record.person.last_name),
            "item": {
                "name": item_record.item.name,
                "description": item_record.item.description,
                "id": item_record.item.id,
            },
            "date_out": item_record.date_checked_out,
            "amount": item_record.amount,
            "id": item_record.id,
            "success": True
        })
    except ValueError, e:
        json_data['success'] = False
    return JsonResponse(json_data)
    
    
    
class ItemListView(TemplateView):
    """docstring for ItemListView"""
    
    template_name = 'inventory/items.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            return super(ItemListView, self).dispatch(request, *args, **kwargs)
        except Exception, e:
            logger.error("%s: %s" % (e.__class__.__name__, e))
            raise e
    
    def get_context_data(self, *args, **kwargs):
        context = super(ItemListView, self).get_context_data(*args, **kwargs)
        
        items = Item.items_in()
        items_out = ItemRecord.users_items_out(self.request.user)
        
        context.update({
            "items_in": items,
            "items_out": items_out,
        })
        
        return context
        