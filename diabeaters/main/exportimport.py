import cgi
import codecs
from django.core.files import File
from xml.etree import ElementTree as etree
from pageblocks.models import TextBlock, HTMLBlock, PullQuoteBlock
from pageblocks.models import ImageBlock, ImagePullQuoteBlock
from diabeaters.quiz.models import Quiz, Question, Answer
from pagetree.models import PageBlock
import os
import tempfile
from zipfile import ZipFile
from pagetree.helpers import get_hierarchy


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
    filename = "pageblocks/%s-description.txt" % block.pageblock().pk
    zipfile.writestr(filename, block.description.encode("utf8"))
    print >> xmlfile, u"""<quiz rhetorical="%s" description_src="%s">""" % (
        block.rhetorical, filename)
    for question in block.question_set.all():
        print >> xmlfile, u"""<question type="%s" ordinality="%s">""" % (
            question.question_type, question.ordinality)
        filename = "pageblocks/%s-%s-text.txt" % (block.pageblock().pk,
                                                  question.pk)
        zipfile.writestr(filename, question.text.encode("utf8"))
        print >> xmlfile, u"<text src='%s' />" % filename

        filename = "pageblocks/%s-%s-explanation.txt" % (block.pageblock().pk,
                                                         question.pk)
        zipfile.writestr(filename, question.explanation.encode("utf8"))
        print >> xmlfile, u"<explanation src='%s' />" % filename

        filename = "pageblocks/%s-%s-introtext.txt" % (block.pageblock().pk,
                                                       question.pk)
        zipfile.writestr(filename, question.intro_text.encode("utf8"))
        print >> xmlfile, u"<introtext src='%s' />" % filename

        for answer in question.answer_set.all():
            print >> xmlfile, (
                u"""<answer label="%s" value="%s" """
                u"""ordinality="%s" correct="%s" />""" % (
                    sanitize(answer.label),
                    answer.value, answer.ordinality, answer.correct))

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

    fd, zip_filename = tempfile.mkstemp(prefix="pagetree-export",
                                        suffix=".zip")
    zipfile = ZipFile(zip_filename, 'w')
    zipfile.writestr("version.txt", "1")

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
    b = HTMLBlock(html=body)
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
    children = node.getchildren()
    assert len(children) == 1 and children[0].tag == "quiz"
    rhetorical = asbool(children[0].get("rhetorical"))
    path = children[0].get("description_src")
    description = zipfile.read(path)
    q = Quiz(rhetorical=rhetorical, description=description)
    q.save()
    for child in children[0].getchildren():
        assert child.tag == "question"
        type = child.get("type")
        ordinality = child.get("ordinality")

        (text, explanation, introtext, answers) = (child.getchildren()[:3]
                                                   + [child.getchildren()[3:]])
        path = text.get("src")
        text = zipfile.read(path)
        path = explanation.get("src")
        explanation = zipfile.read(path)
        path = introtext.get("src")
        introtext = zipfile.read(path)
        question = Question(quiz=q, text=text, question_type=type,
                            ordinality=ordinality, explanation=explanation,
                            intro_text=introtext)
        question.save()
        for answer in answers:
            label = answer.get("label")
            value = answer.get("value")
            ordinality = answer.get("ordinality")
            correct = asbool(answer.get("correct"))
            answer = Answer(question=question, ordinality=ordinality,
                            value=value, label=label, correct=correct)
            answer.save()
    return q

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
    pb = PageBlock(section=section, ordinality=ordinality, label=label,
                   content_object=block)
    pb.save()
    return pb


def import_node(hierarchy, section, zipfile, parent=None):
    slug = section.get("slug")
    label = section.get("label")
    is_root = asbool(section.get("is_root"))
    assert (parent and not is_root) or (is_root and not parent)

    if parent is None:
        s = hierarchy.get_root()
        s.slug = slug
        s.label = label
        s.save()
    else:
        s = parent.append_child(label, slug)
        s.save()

    for child in section.getchildren():
        if child.tag == "pageblock":
            import_pageblock(hierarchy, s, child, zipfile)
        elif child.tag == "section":
            import_node(hierarchy, child, zipfile, parent=s)
        else:
            raise TypeError("Badly formatted import file")

    return s


def import_zip(zipfile):
    if 'site.xml' not in zipfile.namelist():
        raise TypeError("Badly formatted import file")
    if 'version.txt' not in zipfile.namelist():
        raise TypeError("Badly formatted import file")
    if zipfile.read("version.txt") != "1":
        raise TypeError("Badly formatted import file")
    structure = zipfile.read("site.xml")
    structure = etree.fromstring(structure)

    name = structure.get("name")
    base_url = structure.get("base_url")

    hierarchy = get_hierarchy(name=name)
    hierarchy.base_url = base_url
    hierarchy.save()

    for section in structure.getchildren():
        import_node(hierarchy, section, zipfile)

    return hierarchy
