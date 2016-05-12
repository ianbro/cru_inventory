from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Item(models.Model):
    
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    total_amount = models.PositiveIntegerField(default=1)
    amount_left = models.PositiveIntegerField(default=1)
    
    def checkout(self, user, amount):
        return ItemRecord.objects.create(person=user, item=self, amount=amount)
    
    @staticmethod
    def items_in():
        return Item.objects.filter(amount_left__gte=0)
    
    @staticmethod
    def items_out():
        return ItemRecord.objects.filter(date_checked_in__isnull=True)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.amount_left = self.total_amount
        super(Item, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name
        
class ItemRecord(models.Model):
    """docstring for ItemRecord"""
    
    person = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    date_checked_out = models.DateTimeField(auto_now_add=True)
    date_checked_in = models.DateTimeField(null=True, blank=True)
    amount = models.PositiveIntegerField(default=1)
    
    @staticmethod
    def users_items_out(user):
        return Item.items_out().filter(person=user)
    
    def is_checkedin(self):
        if self.date_checked_in is None:
            return False
        else:
            return True
    
    def checkin(self):
        self.date_checked_in = timezone.now()
        item = Item.objects.get(id=self.item.id)
        item.amount_left = item.amount_left + self.amount
        self.save()
        item.save()
        return self
    
    def save(self, *args, **kwargs):
        if not self.date_checked_in is None:
            record = super(ItemRecord, self).save(*args, **kwargs)
            return record
            
        item = Item.objects.get(id=self.item.id)
        if self.amount > item.amount_left:
            raise ValueError("There are not enough %ss left to take %s of them out. There are only %d left." % (self.item, self.amount, self.item.amount_left))
        else:
            record = super(ItemRecord, self).save(*args, **kwargs)
            self.item.amount_left = self.item.amount_left - self.amount
            self.item.save()
            return record
            
    def __str__(self):
        return "%s %s: %d %s" % (self.person.first_name, self.person.last_name, self.amount, self.item.name)
    
    def __repr__(self):
        return "%s %s: %d %s" % (self.person.first_name, self.person.last_name, self.amount, self.item.name)