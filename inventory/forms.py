from django import forms

from inventory.models import Item, ItemRecord, Category

class CreateItemForm(forms.ModelForm):
    
    try:
        categories = Category.objects.leaf_categories()
    except Exception, e:
        categories = []
    
    class Meta:
        model = Item
        exclude = ["date_added", "amount_left"]
        
    category = forms.ModelChoiceField(queryset=categories)