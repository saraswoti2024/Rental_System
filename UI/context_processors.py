# your_app/context_processors.py
from .models import Choice1

def property_types(request):
    return {'nav': Choice1.objects.all()}
