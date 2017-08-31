from django.contrib import admin

from .models import Stance


class StanceAdmin(admin.ModelAdmin):
    model = Stance
    list_display = ['user', 'question',  'choice', 'num_agree']


admin.site.register(Stance, StanceAdmin)
