from otree.urls import urlpatterns
from django.urls import path
from django.http import HttpResponseRedirect

def redirect_to_experiment(request):
    return HttpResponseRedirect('/p/main_experiment/')

urlpatterns = [
    path('', redirect_to_experiment),
] + urlpatterns
