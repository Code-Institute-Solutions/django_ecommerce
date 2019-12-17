from django import template

register = template.Library()

@register.filter(name='update_get')
def update_get(current_get, new_params):
    """
    Updates the given GET parameters with the new ones
    to render an updated URL
    """
    copied_get = current_get.copy()
    for p in new_params.split('&'):
        param = p.split('=')[0]
        value = p.split('=')[1]
        copied_get[param] = value

    return '?' + copied_get.urlencode()

@register.filter(name="get_url_params")
def get_url_params(current_get):
    return True