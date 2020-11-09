from django.contrib import admin
from django.db.models.fields import BinaryField

from .models import User, Bid, Listing, Comment, Category

# Register your models here.

class category(admin.ModelAdmin):
    list_display = ("__str__", "category")

admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Category)


