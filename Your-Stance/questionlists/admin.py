from django.contrib import admin

from .models import QuestionList, QuestionListItem


class QuestionListAdmin(admin.ModelAdmin):
    model = QuestionList
    prepopulated_fields = {'slug': ('name',), }


class QuestionListItemAdmin(admin.ModelAdmin):
    list_display = [ 'question', 'list', ]

admin.site.register(QuestionList, QuestionListAdmin)
admin.site.register(QuestionListItem, QuestionListItemAdmin)
