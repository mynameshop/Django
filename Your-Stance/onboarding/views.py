from django.shortcuts import render
from django.views.generic import View


class EditProfileView(View):
    template_name = 'onboarding/edit_profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class TopQuestionsView(View):
    template_name = 'onboarding/top_questions.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
