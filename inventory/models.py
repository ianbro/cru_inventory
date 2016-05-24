from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
class CategoryManager(models.Manager):
    
    def leaf_categories(self):
        ids = []
        for c in Category.objects.all():
            if not Category.objects.filter(parent_category=c).exists():
                ids.append(c.id)
        return Category.objects.filter(pk__in=ids)
        
    def root_categories(self):
        return Category.objects.filter(parent_category=None)


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
        
    def to_json(self, level=0):
        json = {
            "pk": self.id,
            "name": self.name,
            "level": level,
        }
        if self.category_set.all().exists():
            cats = []
            for cat in self.category_set.all():
                cats.append(cat.to_json(level + 1))
            json["categories"] = cats
        else:
            json["items"] = []
            for item in self.item_set.all():
                json["items"].append(item.to_json(level + 1))
        return json
        
    def save(self, *args, **kwargs):
        if not self.id and not self.parent_category is None:
            if self.name == "%s: Other" % self.parent_category.name:
                super(Category, self).save(*args, **kwargs)
                for item in self.parent_category.item_set.all():
                    item.category = self
                    item.save()
                return self
            else:
                sibling_children = Item.objects.filter(category=self.parent_category)
                if sibling_children.exists():
                    other_cat = Category.objects.get_or_create(name="%s: Other" % self.parent_category.name, parent_category=self.parent_category)
                return super(Category, self).save(*args, **kwargs)
        else:
            return super(Category, self).save(*args, **kwargs)
            
            
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
    
    def checkout(self, person, amount):
        return ItemRecord.objects.create(person=person, item=self, amount=amount)
    
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name
        
    def to_json(self, level=0):
        json = {
            "pk": self.id,
            "name": self.name,
            "description": self.description,
            "date_added": self.date_added.strftime("%D"),
            "total_amount": self.total_amount,
            "amount_left": self.amount_left,
            "level": level
        }
        return json
        
    def save(self, *args, **kwargs):
        sibling_cats = Category.objects.filter(parent_category=self.category)
        if sibling_cats.exists():
            self.category = Category.objects.get_or_create(name="%s: Other" % self.category.name, parent_category=self.category)[0]
        if self.pk is None:
            self.amount_left = self.total_amount
        return super(Item, self).save(*args, **kwargs)

        
class ItemRecord(models.Model):
    """docstring for ItemRecord"""
    
    person = models.CharField(max_length=50)
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
        return "%s: %d %s" % (self.person, self.amount, self.item.name)
    
    def __repr__(self):
        return "%s: %d %s" % (self.person, self.amount, self.item.name)