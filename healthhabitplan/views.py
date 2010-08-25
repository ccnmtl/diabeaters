# Create your views here.
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from models import *

def index(request):
    user = request.user
    if request.user.is_anonymous():
        return HttpResponseRedirect("/accounts/login/")
    return HttpResponse("this is the health habit plan")
