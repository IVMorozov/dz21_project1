from django import template 
import markdown

register = template.Library()

@register.filter
def md_html(md_string):
    """ md to html converter"""
    if not md_string:
        return ''
    md = markdown.Markdown(extensions=['fenced_code', 'codeflite', 'tables'])
    html = md.convert(md_string)
    return html