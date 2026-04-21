from django.shortcuts import render
from .models import HealthUpdate

def home(request):
    updates = HealthUpdate.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'updates': updates})