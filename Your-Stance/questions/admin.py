from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import redirect

from .models import Answer, Question, SuggestedQuestion

# class QuestionAdmin(admin.ModelAdmin):
#     """
#     Model Admin that manages the Question Model
#     """
#
#     model = Question
#     fieldsets = [
#         (None, {'fields': ['question_text', 'slug', 'details']}),
#     ]
#     search_fields = ['question_text']
#     list_display = ['question_text', 'slug', 'details']
#

#
# class AnswerAdmin(admin.ModelAdmin):
#     """
#     Model Admin that manages the Answer Admin
#     """
#     model = Answer
#     list_display = ['question', 'choice', 'user', 'stance', ]

class SuggestedQuestionAdmin(admin.ModelAdmin):
    list_display = ['slug', 'get_username', 'created', 'is_approved_human_readable' ]
    readonly_fields = ['get_username', 'related_question', ]
    fields = ['slug', 'details', 'get_username', 'related_question', ]
    change_form_template = 'questions/admin/change_form.html'
    
    def has_add_permission(self, request):
        return False
    
    def get_urls(self):
        urls = super(SuggestedQuestionAdmin, self).get_urls()
        
        add_urls = [
                           url(r'(?P<id>\d+)/approve/$',
                            self.admin_site.admin_view(self.approve), name="suggest_approve"),
        ]
        return add_urls + urls
    
    def approve(self, request, id):
        
        suggestion = SuggestedQuestion.objects.get(pk=id)
        question = Question(slug=suggestion.slug, details=suggestion.details)
        question.save()
        
        suggestion.related_question = question
        suggestion.save()
        
        return redirect('/admin/questions/suggestedquestion/')
        

admin.site.register(SuggestedQuestion, SuggestedQuestionAdmin)
admin.site.register(Question)
admin.site.register(Answer)
