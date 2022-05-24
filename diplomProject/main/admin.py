from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *
from django.contrib.auth.admin import UserAdmin



class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = News
        fields = '__all__'

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    form = NewsAdminForm

admin.site.register(News, NewsAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Tag)
admin.site.register(LikeDislike)
admin.site.register(Question)
admin.site.register(Answer)

