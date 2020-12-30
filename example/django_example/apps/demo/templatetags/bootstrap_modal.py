import re

from django import template
from django.template.base import token_kwargs, Variable
from django.template.loader import render_to_string


def camel_to_snake(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '-', s).lower()


register = template.Library()


@register.tag
def modal(parser, token):
    """
    Display a Bootstrap modal on the page containing any valid Django template code between begin and end tags.

    Examples:
        {% modal %}
            <p>Look ma! I'm in a modal!</p>
        {% footer %}
            <span>That's great, son. </span><button class="btn btn-default" data-dismiss="modal">Close</button>
        {% endmodal %}

        {% modal %}
            <form method="POST" action="">
                {% csrf_token %}
                {{ form }}
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        {% endmodal %}
    """
    bits = token.split_contents()
    bit_kwargs = token_kwargs(bits[1:], parser)
    modal_id = Variable(str(bit_kwargs.get('modal_id', 'modal')))
    title = Variable(str(bit_kwargs.get('title', None)))
    turbo_frame = Variable(str(bit_kwargs.get('turbo', None)))

    # Fetch all data attributes
    data_attributes = {camel_to_snake(k): Variable(bit_kwargs[k].token) for k in bit_kwargs.keys() if
                       re.match("data[A-Z]", k)}

    nodelist_body = parser.parse(('footer', 'endmodal'))
    token = parser.next_token()
    if token.contents == 'footer':
        nodelist_footer = parser.parse(('endmodal',))
        parser.delete_first_token()
    else:
        nodelist_footer = None

    return ModalNode(modal_id, title, nodelist_body, nodelist_footer, turbo_frame, data_attributes=data_attributes)


class ModalNode(template.Node):

    def __init__(self, modal_id, title, nodelist_body, nodelist_footer, turbo_frame, data_attributes={}):
        self.turbo_frame = turbo_frame
        self.modal_id = modal_id
        self.title = title
        self.nodelist_body = nodelist_body
        self.nodelist_footer = nodelist_footer
        self.data_attributes = data_attributes

    def render(self, context):
        modal_id = self.modal_id.resolve(context) if self.modal_id else 'modal'
        title = self.title.resolve(context) if self.title else None
        turbo_frame_id = self.turbo_frame.resolve(context) if self.turbo_frame else None

        data_attributes = ' '.join([f'{k}="{v.resolve(context)}"' for k, v in self.data_attributes.items()])

        footer = f'<div class="modal-footer">{self.nodelist_footer.render(context)}</div>' if self.nodelist_footer else ''
        return render_to_string('demo/modal.html',
                                context={"modal_id": modal_id, "data_attributes": data_attributes, "title": title,
                                         "body": self.nodelist_body.render(context), "turbo_frame_id": turbo_frame_id, "footer": footer})
