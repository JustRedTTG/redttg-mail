from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()

if User.objects.filter(name='red').exists():
    User.objects.get(name='red').delete()
User.objects.create_superuser('red', 'red')