from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required



from django.db.models import Count
# Create your views here.

def blog(request):

    return render(request, "blog/blog.html")


