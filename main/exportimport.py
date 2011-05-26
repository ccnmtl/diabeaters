import cgi
import codecs
from django.core.files import File
from diabeaters.quiz.models import *
import lxml.etree as etree
from pageblocks.models import *
from pagetree.models import *
import tempfile
from zipfile import ZipFile

def asbool(str):
    return str.lower() == "true"

def sanitize(label):
    return cgi.escape(label, True)
    
def get_all_pageblocks(hierarchy):
    return PageBlock.objects.filter(section__hierarchy=hierarchy)

def text_exporter(block, xmlfile, zipfile):
    filename = "pageblocks/%s.txt" % block.pageblock().pk
    zipfile.writestr(filename, block.body.encode("utf8"))
    print >> xmlfile, """<text src="%s" />""" % filename
def html_exporter(block, xmlfile, zipfile):
    filename = "pageblocks/%s.html" % block.pageblock().pk
    zipfile.writestr(filename, block.html.encode("utf8"))
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
                sanitize(answer.label), answer.value, answer.ordinality, answer.correct)

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
        block.pk, type, sanitize(block.label), block.ordinality)
    export_fn(object, xmlfile, zipfile)
    print >> xmlfile, "</pageblock>"

def export_node(node, xmlfile, zipfile):
    print >> xmlfile, \
        u"""<section slug="%s" label="%s" is_root="%s">""" % (
        node.slug, sanitize(node.label), node.is_root)
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

def text_importer(node, zipfile):
    children = node.getchildren()
    assert len(children) == 1 and children[0].tag == "text"
    path = children[0].get("src")
    body = zipfile.read(path)
    b = TextBlock(body=body)
    b.save()
    return b

def html_importer(node, zipfile):
    children = node.getchildren()
    assert len(children) == 1 and children[0].tag == "html"
    path = children[0].get("src")
    body = zipfile.read(path)
    b = HtmlBlock(html=body)
    b.save()
    return b

def pullquote_importer(node, zipfile):
    children = node.getchildren()
    assert len(children) == 1 and children[0].tag == "text"
    path = children[0].get("src")
    body = zipfile.read(path)    
    b = PullQuoteBlock(body=body)
    b.save()
    return b

def image_importer(node, zipfile):
    children = node.getchildren()
    assert len(children) == 1 and children[0].tag == "img"
    path = children[0].get("src")
    caption = children[0].get("caption")
    file = zipfile.open(path)
    file.size = zipfile.getinfo(path).file_size
    b = ImageBlock(caption=caption, image='')
    b.save_image(File(file))
    b.save()
    return b

def imagepullquote_importer(node, zipfile):
    children = node.getchildren()
    assert len(children) == 1 and children[0].tag == "img"
    path = children[0].get("src")
    caption = children[0].get("caption")
    file = zipfile.open(path)
    file.size = zipfile.getinfo(path).file_size
    b = ImagePullQuoteBlock(caption=caption, image='')
    b.save_image(File(file))
    b.save()
    return b

def quiz_importer(node, zipfile):
    pass

pageblock_importers = {
    'text': text_importer,
    'html': html_importer,
    'pullquote': pullquote_importer,
    'image': image_importer,
    'imagepullquote': imagepullquote_importer,
    'quiz': quiz_importer,
    }

def import_pageblock(hierarchy, section, pageblock, zipfile):
    type = pageblock.get("type")
    label = pageblock.get("label")
    ordinality = pageblock.get("ordinality")

    block = pageblock_importers[type](pageblock, zipfile)
    pb = PageBlock(section=section, ordinality=ordinality, label=label, content_object=block)
    pb.save()
    return pb

def import_node(hierarchy, section, zipfile):
    slug = section.get("slug")
    label = section.get("label")
    is_root = asbool(section.get("is_root"))
    s = Section(label=label, slug=slug, hierarchy=hierarchy, is_root=is_root)
    s.save()
    
    for child in section.iterchildren():
        if child.tag == "pageblock":
            import_pageblock(hierarchy, s, child, zipfile)
        elif child.tag == "section":
            import_node(hierarchy, child, zipfile)
        else:
            raise TypeError("Badly formatted zipfile")

    return s

def import_zip(zipfile):
    if 'site.xml' not in zipfile.namelist():
        raise TypeError("Badly formatted zipfile")
    structure = zipfile.read("site.xml")
    structure = etree.fromstring(structure)

    name = structure.get("name")
    base_url = structure.get("base_url")

    hierarchy = Hierarchy(name=name, base_url=base_url)
    hierarchy.save()

    for section in structure.iterchildren():
        import_node(hierarchy, section, zipfile)

