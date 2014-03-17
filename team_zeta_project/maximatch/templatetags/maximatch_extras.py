from django import template
from maximatch.models import Researcher
from django.contrib.auth.models import User

register = template.Library()


@register.filter(name='is_researcher')
def is_researcher(user_id=None):
    try:
        # If we can't find, the .get() method raises a DoesNotExist exception.
        user = User.objects.get(id=user_id)
        try:
            Researcher.objects.get(user=user)
            return True
        except Researcher.DoesNotExist:
            pass
    except:
        pass
    return False
