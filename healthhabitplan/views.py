# Create your views here.
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from models import *

class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if type(items) == type({}):
                return render_to_response(self.template_name, items, context_instance=RequestContext(request))
            else:
                return items

        return rendered_func

@login_required
@rendered_with('healthhabitplan/index.html')
def index(request):
    user = request.user
    sessions = Session.objects.filter(user=user)
    return dict(user=user,
                sessions=sessions)


@login_required
def new_session(request):
    user = request.user
    s = Session.objects.create(user=user)
    return HttpResponseRedirect("/health-habit-plan/")

@login_required
@rendered_with('healthhabitplan/session.html')
def session(request,id):
    s = get_object_or_404(Session,id=id)
    return dict(session=s,
                categories=Category.objects.all(),
                )

@login_required
def save_magnet(request,id):
    s = get_object_or_404(Session,id=id)
    if request.method == "POST":
        item_id = request.GET['item_id']
        item = get_object_or_404(Item,id=item_id)
        x = request.GET['x']
        y = request.GET['y']
        r = Magnet.objects.filter(session=s,item=item)
        if r.count() > 0:
            m = r[0]
            m.x = x
            m.y = y
            m.save()
        else:
            m = Magnet.objects.create(session=s,item=item,x=x,y=y)
    return HttpResponse("ok");
