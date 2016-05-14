import logging

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
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
        # try:
        #     return super(AddItemView, self).dispatch(request, *args, **kwargs)
        # except Exception, e:
        #     logger.error("%s: %s" % (e.__class__.__name__, e))
        #     raise e
        return super(AddItemView, self).dispatch(request, *args, **kwargs)
            
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
            
            
def ajax_checkout_item(request, *args, **kwargs):
    
    if request.method == "POST":
        json_data = {}
        
        user = request.user
        amount = int(request.POST['amount'])
        item_id = int(request.POST['item_id'])
        
        try:
            item_record = Item.objects.get(id=item_id).checkout(user, amount)
            return HttpResponseRedirect(reverse('inv:items'))
        except ValueError:
            return HttpResponseRedirect("%s?error=true" % reverse('inv:items'))
    else:
        return Http404("Please Don't Do That!")
    
    
def ajax_checkin_item(request, record_id, *args, **kwargs):
    json_data = {}
    
    try:
        item_record = ItemRecord.objects.get(id=record_id).checkin()
        json_data.update({
            "name": item_record.item.name,
            "description": item_record.item.description,
            "total_amount": item_record.item.total_amount,
            "amount_left": item_record.item.amount_left,
            "success": True
        })
    except ItemRecord.DoesNotExist, e:
        json_data['success'] = False
        logger.error("%s: %s" % (e.__class__.__name__, e))
    return JsonResponse(json_data)
    
    
def ajax_useup_item(request, record_id, *args, **kwargs):
    json_data = {}
    
    try:
        item_record = ItemRecord.objects.get(id=record_id).use_up_item()
        json_data.update({
            "name": item_record.item.name,
            "description": item_record.item.description,
            "total_amount": item_record.item.total_amount,
            "amount_left": item_record.item.amount_left,
            "success": True
        })
    except ItemRecord.DoesNotExist, e:
        json_data['success'] = False
        logger.error("%s: %s" % (e.__class__.__name__, e))
    return JsonResponse(json_data)
    
    
class ItemListView(TemplateView):
    """docstring for ItemListView"""
    
    template_name = 'inventory/items.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # try:
        #     return super(ItemListView, self).dispatch(request, *args, **kwargs)
        # except Exception, e:
        #     logger.error("%s: %s" % (e.__class__.__name__, e))
        #     raise e
        return super(ItemListView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(ItemListView, self).get_context_data(*args, **kwargs)
        
        items = Item.objects.items_in()
        items_out = ItemRecord.objects.users_items_out(self.request.user)
        
        context.update({
            "items_in": items,
            "items_out": items_out,
        })
        
        if 'error' in self.request.GET.keys():
            context['item_amount_error'] = True
        
        return context
        