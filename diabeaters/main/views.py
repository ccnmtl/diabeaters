from annoying.decorators import render_to
from diabeaters.main.exportimport import export_zip
from diabeaters.main.exportimport import import_zip
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseNotFound
import os
from pagetree.helpers import (get_hierarchy, get_section_from_path, get_module,
                              needs_submit, submitted)
from zipfile import ZipFile


def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)


def flatpage_hack(request):
    # immediately 404 for about/contact/credits so flatpages
    # handles them and we don't send them to auth first
    return HttpResponseNotFound()


def get_profile(request, path):
    if not request.user.is_anonymous():
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            profile.current_location = path
            profile.save()
    if not request.user.is_anonymous():
        if hasattr(request.user, 'profile'):
            return request.user.profile
        else:
            return None
    return None


def page_reset(request, section):
    # it's a reset request
    for p in section.pageblock_set.all():
        if hasattr(p.block(), 'needs_submit'):
            if p.block().needs_submit():
                p.block().clear_user_submissions(request.user)
    return HttpResponseRedirect(section.get_absolute_url())


def get_form_data(request, prefix):
    data = dict()
    for k in request.POST.keys():
        if k.startswith(prefix):
            # handle lists for multi-selects
            v = request.POST.getlist(k)
            if len(v) == 1:
                data[k[len(prefix):]] = request.POST[k]
            else:
                data[k[len(prefix):]] = v
    return data


def page_post(request, section):
    # user has submitted a form. deal with it
    if request.POST.get('action', '') == 'reset':
        return page_reset(request, section)
    proceed = True
    for p in section.pageblock_set.all():
        if hasattr(p.block(), 'needs_submit'):
            if p.block().needs_submit():
                prefix = "pageblock-%d-" % p.id
                data = get_form_data(request, prefix)
                p.block().submit(request.user, data)
                if hasattr(p.block(), 'redirect_to_self_on_submit'):
                    # semi bug here?
                    # proceed will only be set by the last submittable
                    # block on the page. previous ones get ignored.
                    proceed = not p.block().redirect_to_self_on_submit()
    if proceed:
        return HttpResponseRedirect(section.get_next().get_absolute_url())
    else:
        # giving them feedback before they proceed
        return HttpResponseRedirect(section.get_absolute_url())


@login_required
@render_to('main/page.html')
def page(request, path):
    section = get_section_from_path(path)
    # redirects to first (welcome) page for parent nodes
    section = section.get_first_leaf()
    h = get_hierarchy()

    profile = get_profile(request, path)

    if request.method == "POST":
        return page_post(request, section)
    else:
        return dict(section=section,
                    needs_submit=needs_submit(section),
                    module=get_module(section),
                    profile=profile,
                    is_submitted=submitted(section, request.user),
                    root=h.get_root())


@login_required
@render_to('main/edit_page.html')
def edit_page(request, path):
    section = get_section_from_path(path)
    h = get_hierarchy()
    return dict(section=section,
                module=get_module(section),
                root=h.get_root())


@login_required
@render_to('main/instructor_page.html')
def instructor_page(request, path):
    section = get_section_from_path(path)
    h = get_hierarchy()
    quizzes = [p.block() for p in section.pageblock_set.all()
               if hasattr(p.block(), 'needs_submit') and
               p.block().needs_submit()]
    return dict(section=section,
                quizzes=quizzes,
                module=get_module(section),
                root=h.get_root())


@login_required
@render_to('main/home.html')
def home(request):
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
    else:
        profile = None
    return dict(profile=profile)


def index(request):
    return HttpResponseRedirect("/intro/")


@login_required
def health_habit_plan(request):
    return HttpResponse("not implemented yet")


@staff_required()
def export(request):
    section = get_section_from_path('/')
    zip_filename = export_zip(section.hierarchy)

    with open(zip_filename) as zipfile:
        resp = HttpResponse(zipfile.read())
    resp['Content-Disposition'] = ("attachment; filename=%s.zip"
                                   % section.hierarchy.name)

    os.unlink(zip_filename)
    return resp


@staff_required()
@render_to("main/import.html")
def import_(request):
    if request.method == "GET":
        return {}
    file = request.FILES['file']
    zipfile = ZipFile(file)
    hierarchy = import_zip(zipfile)

    url = hierarchy.get_absolute_url()
    url = '/' + url.lstrip('/')  # sigh
    return HttpResponseRedirect(url)
