from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()

if not User.objects.filter(name='red').exists():
    User.objects.create_superuser('red', 'red')