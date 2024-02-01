# decorators.py
from django.contrib.auth.decorators import user_passes_test

def group_required(groups=[]):
    """
    Decorator to check if the user belongs to any of the specified groups.
    """
    return user_passes_test(lambda user: any(group in user.groups.values_list('name', flat=True) for group in groups))
