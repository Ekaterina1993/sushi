from django.contrib import admin
from .models import Section, Product
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class PreviewImageMixin(object):
    def thumb(self, obj):
        return render_to_string('catalog/elements/admin/thumb.html', {
            'image': obj.image
        })

    thumb.allow_tags = True

    def headshot_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image.url,
            width=obj.image.width / 2,
            height=obj.image.height / 2,
            )
    )


class SectionAdmin(admin.ModelAdmin, PreviewImageMixin):
    list_display = ['title', 'slug', 'thumb', 'created']
    readonly_fields = ["headshot_image"]
    prepopulated_fields = {'slug': ('title',), }



admin.site.register(Section, SectionAdmin)


class ProductAdmin(admin.ModelAdmin, PreviewImageMixin):
    pass


admin.site.register(Product, ProductAdmin)
