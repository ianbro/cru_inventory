import logging
import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string

from inventory.models import Item, ItemRecord, Category
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
        
        person = request.POST['person']
        amount = int(request.POST['amount'])
        item_id = int(request.POST['item_id'])
        
        try:
            item_record = Item.objects.get(id=item_id).checkout(person, amount)
            return JsonResponse({
                "success": True,
                "item_record": item_record.to_json()
            })
        except ValueError, e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            })
    else:
        return HttpResponseBadRequest("Please Don't Do That!")
    
    
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
    
    def dispatch(self, request, *args, **kwargs):
        # try:
        #     return super(ItemListView, self).dispatch(request, *args, **kwargs)
        # except Exception, e:
        #     logger.error("%s: %s" % (e.__class__.__name__, e))
        #     raise e
        return super(ItemListView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(ItemListView, self).get_context_data(*args, **kwargs)
        
        items_out = Item.objects.items_out()
        
        categories = Category.objects.root_categories()
        json_categories = []
        for cat in categories:
            json_categories.append(cat.to_json())
        
        context.update({
            "categories_json": json.dumps(json_categories),
            "categories_python": categories,
            "items_out": items_out,
        })
        
        if 'error' in self.request.GET.keys():
            context['item_amount_error'] = True
        
        return context
        
        
def ajax_get_items_by_category(request, *args, **kwargs):
    if request.method == "POST":
        return HttpResponseBadRequest("Please don't do that.")
    else:
        cat_id = request.GET.get("cat_id", None)
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            items = Item.objects.filter(category=category)
            sub_categories = category.category_set.all()
            return JsonResponse({
                "items": [i.to_json() for i in items],
                "sub_categories": [c.to_json() for c in sub_categories],
            })
        else:
            root_categories = Category.objects.root_categories()
            return JsonResponse({
                "items": [],
                "sub_categories": [c.to_json() for c in root_categories],
            })
            
            
def ajax_get_items_by_category_html(request, *args, **kwargs):
    if request.method == "POST":
        return HttpResponseBadRequest("Please don't do that.")
    else:
        html = ""
        
        def element_render(type, element):
            if type == "i":
                template = "inventory/elements/item.html"
                return render_to_string(template, {"item": element})
            elif type == "c":
                template = "inventory/elements/category.html"
                return render_to_string(template, {"category": element})
            elif type == "r":
                template = "inventory/elements/record.html"
                return render_to_string(template, {"item_record": element})
            else:
                return "Item type '%s' is not supported" % type
        
        ids = request.GET.get("ids", None)
        if ids:
            ids = [i for i in ids.split(";")]
            
            for id in ids:
                cat_or_item = id.split(":")[0]
                id = int(id.split(":")[1])
                
                element = None
                if cat_or_item == "i":
                    # It's an item
                    element = Item.objects.get(id=id)
                elif cat_or_item == "c":
                    # It's a category
                    element = Category.objects.get(id=id)
                elif cat_or_item == "r":
                    # It's an ItemRecord
                    element = ItemRecord.objects.get(id=id)
                html = html + "\n" + element_render(cat_or_item, element)    
                
            return HttpResponse(html)
        else:
            return HttpResponse("No data to show.")
            
        
def ajax_get_list_html(request, *args, **kwargs):
    if request.method == "POST":
        return HttpResponseBadRequest("Please don't do that.")
    else:
        cat_id = request.GET.get("cat_id", None)
        template = "inventory/components/list_itemsin.html"
        
        if cat_id:
            category = Category.objects.get(id=cat_id)
            context = {
                "html_id": category.id,
                "category": category
            }
            return HttpResponse(render_to_string(template, context))
        else:
            context = {
                "html_id": "root_list"
            }
            return HttpResponse(render_to_string(template, context))
            
            
def ajax_get_list_items_out_json(request, *args, **kwargs):
    if request.method == "POST":
        return HttpResponseBadRequest("Please don't do that.")
    else:
        items_out = [i.to_json() for i in Item.objects.items_out()]
        return JsonResponse({"data": items_out})
            

def ajax_get_list_items_out_html(request, *args, **kwargs):
    if request.method == "POST":
        return HttpResponseBadRequest("Please don't do that.")
    else:
        item_ids = request.GET.get("ids", None)
        template = "inventory/elements/item_out.html"
        html = ""
        ids = [i for i in item_ids.split(";")]
        
        for id in ids:
            cat_or_item = id.split(":")[0]
            id = int(id.split(":")[1])
            
            if cat_or_item == "r":
                record = ItemRecord.objects.get(id=id)
                html = html + "\n" + render_to_string(template, { "record": record })
            else:
                html = html + "\n" + "<!-- Unknown Type %d. It must only be type 'r'. -->" % id
            
        return HttpResponse(html)
        

def ajax_get_records_by_item_html(request, *args, **kwargs):
    if request.method == "POST":
        return HttpResponseBadRequest("Please don't do that.")
    else:
        item_ids = request.GET.get("ids", None)
        template = "inventory/elements/record_for_item.html"
        html = ""
        ids = [i for i in item_ids.split(";")]
        
        for id in ids:
            cat_or_item = id.split(":")[0]
            id = int(id.split(":")[1])
            
            if cat_or_item == "r":
                record = ItemRecord.objects.get(id=id)
                html = html + "\n" + render_to_string(template, { "record": record })
            else:
                html = html + "\n" + "<!-- Unknown Type %d. It must only be type 'r'. -->" % id
            
        return HttpResponse(html)