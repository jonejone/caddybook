from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic.base import View

import simplejson

from caddybook.books.forms import HolePositionFormAjax
from caddybook.books.models import Hole, Course
from caddybook.books.views import _auth_course


class SetHolePositionView(View):
    def post(self, request, **kwargs):

        course = get_object_or_404(Course,
                                   slug=kwargs['slug'])

        hole = Hole.objects.get(course=course,
                                position=kwargs['position'])

        if not _auth_course(request.user, course):
            return HttpResponse(simplejson.dumps({'success': False,
                                'error': 'Access denied'}),
                                mimetype='application/javascript')

        form = HolePositionFormAjax(request.POST, hole=hole)
        response_dict = {'success': False, 'error': None}

        if form.is_valid():
            h = form.save()
            response_dict['success'] = True
            response_dict['message'] = 'Saved succesfully'
            response_dict['distance'] = h.gps_distance()
        else:
            response_dict['error'] = 'Form did not validate'

        return HttpResponse(simplejson.dumps(response_dict),
                            mimetype='application/javascript')
