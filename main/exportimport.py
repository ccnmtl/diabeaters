import codecs
from diabeaters.quiz.models import *
import lxml.etree as etree
from pageblocks.models import *
from pagetree.models import PageBlock
import tempfile
from zipfile import ZipFile

def get_all_pageblocks(hierarchy):
    return PageBlock.objects.filter(section__hierarchy=hierarchy)

def text_exporter(block, xmlfile, zipfile):
    print >> xmlfile, block.body
def html_exporter(block, xmlfile, zipfile):
    filename = "pageblocks/%s.html" % block.pageblock().pk
    zipfile.writestr(filename, block.html)
    print >> xmlfile, """<html src="%s" />""" % filename
def image_exporter(block, xmlfile, zipfile):
    filename = os.path.basename(block.image.file.name)
    filename = "pageblocks/%s-%s" % (block.pk, filename)
    zipfile.write(block.image.file.name, arcname=filename)
    print >> xmlfile, \
        u"""<img src="%s" caption="%s" />""" % (
        filename, block.caption)
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

def export_zip(hierarchy):
    root = hierarchy.get_root()

    fd, zip_filename = tempfile.mkstemp(prefix="pagetree-export", suffix=".zip")
    zipfile = ZipFile(zip_filename, 'w')

    fd, xml_filename = tempfile.mkstemp(prefix="pagetree-site", suffix=".xml")
    xmlfile = codecs.open(xml_filename, 'w', encoding='utf8')

    print >> xmlfile, \
        u"""<hierarchy name="%s" base_url="%s">""" % (
        hierarchy.name, hierarchy.base_url)

    export_node(root, xmlfile, zipfile)
    print >> xmlfile, "</hierarchy>"

    xmlfile.close()
    zipfile.write(xml_filename, arcname="site.xml")
    os.unlink(xml_filename)

    zipfile.close()
    return zip_filename

def import_zip(zipfile):
    if 'site.xml' not in zipfile.namelist():
        raise TypeError("Badly formatted zipfile")
    structure = etree.fromstring(zipfile.read("site.xml"))
    import pdb; pdb.set_trace()
