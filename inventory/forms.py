from django import forms

from inventory.models import Item, ItemRecord

class CreateItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        exclude = ["date_added", "amount_left"]