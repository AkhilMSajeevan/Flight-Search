from django import template

register = template.Library()

@register.inclusion_tag('tree_node.html')
def render_tree(nodes):
    return {'nodes': nodes}
