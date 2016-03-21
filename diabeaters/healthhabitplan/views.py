from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from models import Session, Category, Item, Magnet
from django.core.urlresolvers import reverse
from pagetree.helpers import get_hierarchy


@login_required
def index(request):
    user = request.user
    # let's just send them to the most recent session
    newest = Session.objects.filter(user=user).order_by("-id")
    if newest.count() == 0:
        # create one
        return HttpResponseRedirect(reverse('health-habit-plan-new-session'))
    else:
        return HttpResponseRedirect(
            reverse('health-habit-plan-session', args=[newest[0].id]))


@login_required
def new_session(request):
    user = request.user
    s = Session.objects.create(user=user)
    return HttpResponseRedirect(
        reverse('health-habit-plan-session', args=[s.id]))


@login_required
def del_session(request, id=id):
    s = Session.objects.get(id=id)
    s.delete()
    return HttpResponseRedirect(reverse('health-habit-plan-index'))


@login_required
def session(request, id):
    s = get_object_or_404(Session, id=id)
    h = get_hierarchy()
    return render(request, 'healthhabitplan/session.html',
                  dict(session=s,
                       sessions=Session.objects.filter(user=request.user),
                       categories=Category.objects.all(),
                       root=h.get_root()))


@login_required
def all_sessions(request):
    h = get_hierarchy()
    sessions = Session.objects.filter(user=request.user)
    return render(request, 'healthhabitplan/all_sessions.html',
                  dict(sessions=sessions, categories=Category.objects.all(),
                       root=h.get_root()))


@login_required
def save_magnet(request, id):
    s = get_object_or_404(Session, id=id)
    if request.method == "POST":
        item_id = request.GET['item_id']
        item = get_object_or_404(Item, id=item_id)
        x = request.GET['x']
        y = request.GET['y']
        r = Magnet.objects.filter(session=s, item=item)
        if r.count() > 0:
            m = r[0]
            m.x = x
            m.y = y
            m.save()
        else:
            m = Magnet.objects.create(session=s, item=item, x=x, y=y)
    return HttpResponse("ok")


@login_required
def delete_magnet(request, id):
    s = get_object_or_404(Session, id=id)
    if request.method == "POST":
        item_id = request.GET['item_id']
        item = get_object_or_404(Item, id=item_id)
        r = Magnet.objects.filter(session=s, item=item)
        if r.count() > 0:
            m = r[0]
            m.delete()
    return HttpResponse("ok")
