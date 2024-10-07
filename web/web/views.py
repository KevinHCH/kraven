from django.shortcuts import render
from .models import Jobs


# Create your views here.
def index(request):
    jobs = Jobs.objects.all()
    return render(request, "index.html", {"jobs": jobs})
