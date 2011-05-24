from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
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

def flatpage_hack(request):
    # immediately 404 for about/contact/credits so flatpages
    # handles them and we don't send them to auth first
    return HttpResponseNotFound()

@login_required
@rendered_with('main/page.html')
def page(request,path):
    section = get_section_from_path(path)
    section = section.get_first_leaf()  # redirects to first (welcome) page for parent nodes
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
        if request.POST.get('action','') == 'reset':
            # it's a reset request
            for p in section.pageblock_set.all():
                if hasattr(p.block(),'needs_submit'):
                    if p.block().needs_submit():
                        p.block().clear_user_submissions(request.user)
            return HttpResponseRedirect(section.get_absolute_url())
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




@login_required
@rendered_with('main/edit_page.html')
def edit_page(request,path):
    section = get_section_from_path(path)
    h = get_hierarchy()
    return dict(section=section,
                module=get_module(section),
                root=h.get_root())

@login_required
@rendered_with('main/instructor_page.html')
def instructor_page(request,path):
    section = get_section_from_path(path)
    h = get_hierarchy()
    quizzes = [p.block() for p in section.pageblock_set.all() if hasattr(p.block(),'needs_submit') and p.block().needs_submit()]
    return dict(section=section,
                quizzes=quizzes,
                module=get_module(section),
                root=h.get_root())

@login_required
@rendered_with('main/home.html')
def home(request):
    if hasattr(request.user,'get_profile'):
        profile=request.user.get_profile()
    else:
        profile=None
    return dict(profile=profile)

def index(request):
    return HttpResponseRedirect("/intro/")

@login_required
def health_habit_plan(request):
    return HttpResponse("not implemented yet")

from pagetree.models import PageBlock
def get_all_pageblocks(hierarchy):
    return PageBlock.objects.filter(section__hierarchy=hierarchy)

from pageblocks.models import *
from diabeaters.quiz.models import *
def text_exporter(block, xmlfile, zipfile):
    print >> xmlfile, block.body
def html_exporter(block, xmlfile, zipfile):
    filename = "pageblocks/%s.html" % block.pageblock().pk
    zipfile.writestr(filename, block.html)
    print >> xmlfile, """<html src="%s" />""" % filename
def image_exporter(block, xmlfile, zipfile):
    filename = os.path.basename(block.image.file.name)
    filename = "pageblocks/%s" % filename
    zipfile.write(block.image.file.name, arcname=filename)
    print >> xmlfile, \
        u"""<img src="%s" caption="%s" alt="%s" />""" % (
        filename, block.caption, block.alt)
def quiz_exporter(block, xmlfile, zipfile):
    print >> xmlfile, u"""<quiz rhetorical="%s">""" % block.rhetorical
    print >> xmlfile, block.description
    for question in block.question_set.all():
        print >> xmlfile, u"""<question type="%s" ordinality="%s">""" % (
            question.question_type, question.ordinality)
        print >> xmlfile, u"<text>\n%s\n</text>" % question.text
        print >> xmlfile, u"<explanation>\n%s\n</explanation>" % question.explanation
        print >> xmlfile, u"<introtext>\n%s\n</introtext>" % question.intro_text
        for answer in question.answer_set.all():
            print >> xmlfile, \
                u"""<answer label="%s" value="%s" ordinality="%s" correct="%s" />""" % (
                answer.label, answer.value, answer.ordinality, answer.correct)

        print >> xmlfile, "</question>"
    print >> xmlfile, "</quiz>"
pageblock_exporters = {
    TextBlock: ('text', text_exporter),
    HTMLBlock: ('html', html_exporter),
    PullQuoteBlock: ('pullquote', text_exporter),
    ImageBlock: ('image', image_exporter),
    ImagePullQuoteBlock: ('imagepullquote', image_exporter),
    Quiz: ('quiz', quiz_exporter),
    }
def export_block(block, xmlfile, zipfile):
    object = block.content_object
    type, export_fn = pageblock_exporters[object.__class__]
    print >> xmlfile, \
        u"""<pageblock id="%s" type="%s" label="%s" ordinality="%s">""" % (
        block.pk, type, block.label, block.ordinality)
    export_fn(object, xmlfile, zipfile)
    print >> xmlfile, "</pageblock>"
def export_node(node, xmlfile, zipfile):
    print >> xmlfile, \
        u"""<section slug="%s" label="%s">""" % (
        node.slug, node.label)
    for block in node.pageblock_set.all():
        export_block(block, xmlfile, zipfile)
    for child in node.get_children():
        export_node(child, xmlfile, zipfile)
    print >> xmlfile, "</section>"

from zipfile import ZipFile
import tempfile
import codecs
def export(request):
    hierarchy = request.get_host()
    section = get_section_from_path('/', hierarchy=hierarchy)
    root = section.hierarchy.get_root()
    hierarchy = section.hierarchy

    fd, zip_filename = tempfile.mkstemp(prefix="pagetree-export", suffix=".zip")
    zipfile = ZipFile(zip_filename, 'w')

    fd, xml_filename = tempfile.mkstemp(prefix="pagetree-site", suffix=".xml")
    xmlfile = codecs.open(xml_filename, 'w', encoding='utf8')

    print >> xmlfile, "<hierarchy>"
    export_node(root, xmlfile, zipfile)
    print >> xmlfile, "</hierarchy>"

    xmlfile.close()
    zipfile.write(xml_filename, arcname="site.xml")
    os.unlink(xml_filename)

    zipfile.close()
    with open(zip_filename) as zipfile:
        resp = HttpResponse(zipfile.read())
    resp['Content-Disposition'] = "attachment; filename=%s.zip" % hierarchy.name
    return resp
