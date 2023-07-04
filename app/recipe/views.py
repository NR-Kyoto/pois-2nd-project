from django.shortcuts import render
from django.http import HttpResponse

from .scheduler import RecipeScheduler

def test(request):
    scheduler = RecipeScheduler(['Hamburger', 'ConsommeSoup'])
    schedule = scheduler.scheduling()
    # print(schedule)

    return HttpResponse(schedule)