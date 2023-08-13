try:
    from functools import wraps
except:
    from django.utils.functional import wraps

from django.http import Http404
from django.db.models import Q
from users.models import Wez

def group_required(wez=[]):
    def decorator(func):
        def inner_decorator(request,*args, **kwargs):
            for x in wez:
                test=Wez.objects.get(name=x)
                if Q(test == request.user.wez.name):
                    return func(request, *args, **kwargs)
                break            
            raise Http404()
        
        return wraps(func)(inner_decorator)
    
    return decorator