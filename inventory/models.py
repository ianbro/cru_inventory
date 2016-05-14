from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class CategoryManager(models.Manager):
    
    def leaf_categories(self):
        ids = []
        for c in Category.objects.all():
            if not Category.objects.filter(parent_category=c).exists():
                ids.append(c.id)
        return Category.objects.filter(pk__in=ids)


class Category(models.Model):
    
    objects = CategoryManager()
    
    name = models.CharField(max_length=55)
    parent_category = models.ForeignKey("Category", null=True, blank=True)
    
    def is_leaf_category(self):
        if Category.objects.leaf_categories().filter(pk=self.pk).exists():
            return True
        else:
            return False
            
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name
            
            
class ItemManager(models.Manager):
    
    def items_out(self):
        return ItemRecord.objects.filter(date_checked_in__isnull=True)
        
    def items_in(self):
        return Item.objects.filter(amount_left__gte=0)


class Item(models.Model):
    
    objects = ItemManager()
    
    name = models.CharField(max_length=55)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    total_amount = models.PositiveIntegerField(default=1)
    amount_left = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category)
    
    def checkout(self, user, amount):
        return ItemRecord.objects.create(person=user, item=self, amount=amount)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.amount_left = self.total_amount
        super(Item, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name
        

class ItemRecordManager(models.Manager):
    
    def users_items_out(self, user):
        return Item.objects.items_out().filter(person=user)

        
class ItemRecord(models.Model):
    """docstring for ItemRecord"""
    
    objects = ItemRecordManager()
    
    person = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    date_checked_out = models.DateTimeField(auto_now_add=True)
    date_checked_in = models.DateTimeField(null=True, blank=True)
    amount = models.PositiveIntegerField(default=1)
    used_up = models.NullBooleanField()
    
    def use_up_item(self):
        item = Item.objects.get(id=self.item.id)
        item.total_amount -= self.amount
        item.save()
        self.date_checked_in = timezone.now()
        self.used_up = True
        self.save()
        if item.total_amount == 0:
            item.delete()
        return self
    
    def is_checkedin(self):
        if self.date_checked_in is None:
            return False
        else:
            return True
    
    def checkin(self):
        self.date_checked_in = timezone.now()
        item = Item.objects.get(id=self.item.id)
        item.amount_left = item.amount_left + self.amount
        self.used_up = False
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