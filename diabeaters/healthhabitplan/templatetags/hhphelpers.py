from django import template
from diabeaters.healthhabitplan.models import Magnet

register = template.Library()


class MagnetExistsForSessionNode(template.Node):
    def __init__(self, session, item, nodelist_true, nodelist_false=None):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.session = session
        self.item = item

    def render(self, context):
        s = context[self.session]
        i = context[self.item]
        if Magnet.objects.filter(session=s, item=i).count():
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


@register.tag('if_magnet_for_item_exists')
def accessible(parser, token):
    session = token.split_contents()[1:][0]
    item = token.split_contents()[1:][1]
    nodelist_true = parser.parse(('else', 'endif_magnet_for_item_exists'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif_magnet_for_item_exists', ))
        parser.delete_first_token()
    else:
        nodelist_false = None
    return MagnetExistsForSessionNode(session, item, nodelist_true,
                                      nodelist_false)
