# app_blog/admin.py
from django.contrib import admin
from django.shortcuts import get_object_or_404

from .models import Category, Article, ArticleImage
from .forms import ArticleImageForm


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'slug')
    fieldsets = (
        (None, {
            'fields': ('category', 'slug'),
        }),
    )
    # ✨ ОТУТ ВИКОНАНО ЗАВДАННЯ:
    prepopulated_fields = {'slug': ('category',)}   # ← автозаповнення слага з назви


admin.site.register(Category, CategoryAdmin)


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    form = ArticleImageForm
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('title', 'image'),
        }),
    )


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title' ,'description', 'pub_date', 'slug', 'main_page', 'category')
    inlines = [ArticleImageInline]

    multiupload_form = True
    multiupload_list = False

    prepopulated_fields = {'slug': ('title',)}   # автозаповнення слага статті
    raw_id_fields = ('category',)

    fieldsets = (
        (None, {
            'fields': ('pub_date', 'title', 'description', 'main_page', 'category'),
        }),
        ('Додатково', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('slug',),
        }),
    )

    def delete_file(self, pk, request):
        """Delete an image."""
        obj = get_object_or_404(ArticleImage, pk=pk)
        return obj.delete()


admin.site.register(Article, ArticleAdmin)
