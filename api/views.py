from django.shortcuts import render
from django.http import JsonResponse
from .services.auth import Auth
# Create your views here.
from django.contrib.auth.models import User

def index(request):
    return JsonResponse({
        'Authentication': '/auth',
        'Account' : '/account',
        'Comment' : '/comment',
        'Likes' : '/likes',
        'Images' : '/images',
    })

