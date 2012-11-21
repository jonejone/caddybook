from django.shortcuts import get_object_or_404
from django.http import HttpResponse

import simplejson

from caddybook.books.forms import HolePositionFormAjax
from caddybook.books.models import Hole, Course


def set_hole_geoposition(request, slug, position):
    course = get_object_or_404(Course,
        slug=slug, active=True)

    hole = Hole.objects.get(course=course,
        position=position)

    response_dict = {'success': False, 'error': None}

    if request.method == 'POST':
        form = HolePositionFormAjax(request.POST, hole=hole)

        if form.is_valid():
            h = form.save()
            response_dict['success'] = True
            response_dict['message'] = 'Saved succesfully'
            response_dict['distance'] = h.gps_distance()
        else:
            response_dict['error'] = 'Form did not validate'
    else:
        response_dict['error'] = 'Only POST accepted'


    return HttpResponse(simplejson.dumps(response_dict),
        mimetype='application/javascript')
