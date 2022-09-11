from django.contrib import admin
from django.utils.html import format_html

from adminsortable2.admin import SortableAdminMixin, SortableStackedInline

from .models import (
    WebsiteInfo,
    Category,
    Collection,
    Product,
    ProductImage,
    CustomSpecification,
    AdditionalSpecificationCollection,
    AdditionalSpecificationProduct,
    Slider,
)

admin.site.register(CustomSpecification)


@admin.register(WebsiteInfo)
class WebsiteInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AdditionalSpecificationProductInline(SortableStackedInline):
    model = AdditionalSpecificationProduct
    extra = 1


class AdditionalSpecificationCollectionInline(SortableStackedInline):
    model = AdditionalSpecificationCollection
    extra = 1


class ProductImageInline(SortableStackedInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(SortableAdminMixin, admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(f'<img src="{object.productimage_set.all()[0].image.url}" width="100" />')

    thumbnail.short_description = 'Фото'

    fieldsets = (
        (None, {
            'fields': ('category', 'collection', 'name', 'description', 'price', 'instruction', 'slug', 'is_published')
        }),
        ('ХАРАКТЕРИСТИКИ', {
            'fields': ('material', 'color', 'patina', 'made_in', 'size'),
        }),
    )
    list_display = ['thumbnail', 'name', 'price', 'category', 'collection', 'is_published']
    list_display_links = ['thumbnail', 'name']
    list_filter = ['category', 'collection', 'is_published']
    list_editable = ['price', 'category', 'collection', 'is_published']
    search_fields = ['name']
    inlines = [AdditionalSpecificationProductInline, ProductImageInline]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Collection)
class CollectionAdmin(SortableAdminMixin, admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(f'<img src="{object.image.url}" width="100" />')

    thumbnail.short_description = 'Фото'

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'image', 'instruction', 'slug', 'is_published')
        }),
        ('ХАРАКТЕРИСТИКИ', {
            'fields': ('material', 'color', 'patina', 'made_in', 'bed_size', 'drawer_size', 'wardrobe_size'),
        }),
    )
    list_display = ['thumbnail', 'name', 'price', 'is_published']
    list_display_links = ['thumbnail', 'name']
    list_filter = ['is_published']
    list_editable = ['price', 'is_published']
    search_fields = ['name']
    inlines = [AdditionalSpecificationCollectionInline]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    def thumbnail(self, object):
        if object.image:
            return format_html(f'<img src="{object.image.url}" width="100" />')
        return 'Фото нет'

    thumbnail.short_description = 'Фото'

    list_display = ['thumbnail', 'name', 'is_published']
    list_display_links = ['thumbnail', 'name']
    list_filter = ['is_published']
    list_editable = ['is_published']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Slider)
class SliderAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['product', 'is_published']
    list_editable = ['is_published']
