from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    total_amount = models.PositiveIntegerField(default=1)
    amount_left = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.name
        
class ItemRecord(models.Model):
    """docstring for ItemRecord"""
    
    person = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    date_checked_out = models.DateTimeField(auto_now_add=True)
    date_checked_in = models.DateTimeField(auto_now=True, null=True, blank=True)
    amount = models.PositiveIntegerField(default=1)
    
    def save(self, *args, **kwargs):
        if self.amount > self.item.amount_left:
            raise ValueError("There are not enough %ss left to take %d of them out. There are only %d left." % (self.item, self.amount, self.item.amount_left))
        else:
            record = super(ItemRecord, self).save(*args, **kwargs)
            self.item.amount_left = self.item.amount_left - self.amount
            self.item.save()
            return record
            
    def __str__(self):
        return "%s %s: %d %s" % (self.person.first_name, self.person.last_name, self.amount, self.item.name)