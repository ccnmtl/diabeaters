from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from pagetree.helpers import get_hierarchy, get_section_from_path, get_module, needs_submit, submitted
from models import UserProfile

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

@rendered_with('main/page.html')
def page(request,path):
    section = get_section_from_path(path)
    h = get_hierarchy()

    if not request.user.is_anonymous():
        try:
            profile = request.user.get_profile()
            profile.current_location = path
            profile.save()
        except UserProfile.DoesNotExist:
            pass
    profile = None

    if not request.user.is_anonymous():
        try:
            profile = request.user.get_profile()
        except UserProfile.DoesNotExist:
            pass

    if request.method == "POST":
        # user has submitted a form. deal with it
        proceed = True
        for p in section.pageblock_set.all():
            if hasattr(p.block(),'needs_submit'):
                if p.block().needs_submit():
                    prefix = "pageblock-%d-" % p.id
                    data = dict()
                    for k in request.POST.keys():
                        if k.startswith(prefix):
                            # handle lists for multi-selects
                            v = request.POST.getlist(k)
                            if len(v) == 1:
                                data[k[len(prefix):]] = request.POST[k]
                            else:
                                data[k[len(prefix):]] = v
                    p.block().submit(request.user,data)
                    if hasattr(p.block(),'redirect_to_self_on_submit'):
                        # semi bug here?
                        # proceed will only be set by the last submittable
                        # block on the page. previous ones get ignored.
                        proceed = not p.block().redirect_to_self_on_submit()
        if proceed:
            return HttpResponseRedirect(section.get_next().get_absolute_url())
        else:
            # giving them feedback before they proceed
            return HttpResponseRedirect(section.get_absolute_url())
    else:
        return dict(section=section,
                    needs_submit=needs_submit(section),
                    module=get_module(section),
                    profile=profile,
                    is_submitted=submitted(section,request.user),
                    root=h.get_root())


@rendered_with('main/edit_page.html')
def edit_page(request,path):
    section = get_section_from_path(path)
    h = get_hierarchy()
    return dict(section=section,
                module=get_module(section),
                root=h.get_root())

@rendered_with('main/home.html')
def home(request):
    if hasattr(request.user,'get_profile'):
        profile=request.user.get_profile()
    else:
        profile=None
    return dict(profile=profile)

def index(request):
    return HttpResponseRedirect("/intro/")

def health_habit_plan(request):
    return HttpResponse("not implemented yet")
