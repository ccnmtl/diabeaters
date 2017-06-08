from models import Category, Item, Session, Magnet

from django.contrib import admin


class ItemInline(admin.StackedInline):
    model = Item
    extra = 2


class CategoryAdmin(admin.ModelAdmin):
    inlines = [ItemInline, ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Session)
admin.site.register(Magnet)
