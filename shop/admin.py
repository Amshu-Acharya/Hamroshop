from django.contrib import admin
from .models import *

# Register your models here.

class ProductHasImageInline(admin.StackedInline):
    model = ProductHasImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductHasImageInline,
    ]
admin.site.register(Menu)
admin.site.register(Banner)

admin.site.register(Category)
admin.site.register(Product,ProductAdmin)#mathi wala ko class lai add garnu parcha.
