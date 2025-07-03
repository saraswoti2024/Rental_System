# your_app/context_processors.py
from .models import property_post

##sabai file ma work garxa jaba pass garda
def property_types(request):
    link = property_post.objects.filter(is_approved=True)
    return dict(link=link)
    
