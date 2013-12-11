from django import template
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.utils.safestring import mark_safe


def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return mark_safe(simplejson.dumps(object))

register = template.Library()
register.filter('jsonify', jsonify)
