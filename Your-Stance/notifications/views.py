from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Notification

@login_required()
def notifications(request):
    notifs = Notification.objects.prefetch_related('user_to', \
                    'user_to__profile', 
                    'user_from', 
                    'user_from__profile',
                    'stance',
                    'comment')\
        .filter(user_to=request.user).order_by('-created')
    request.user.profile.read_all_notifs()
    return render(request, 'notifications/notifications.html', {'notifications': notifs})

