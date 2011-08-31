from django.contrib.auth.models import User

def user_count(request):
    return {
        'user_count': User.objects.count(),
    }
