from django.views.generic.base import TemplateView, View
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
import simplejson

from caddybook.books.models import Course, Hole
from caddybook.books.views import _auth_course
from caddybook.books.forms import HoleForm, HoleGalleryImageForm, HolePositionForm


class EditHoleView(View):
    template_name = 'books/hole/edit.html'

    def get_course_and_hole(self, args):
        course_slug = args.get('slug')
        hole_position = int(args.get('position'))

        course = get_object_or_404(Course, slug=course_slug)
        hole = get_object_or_404(Hole, course=course,
            position=hole_position)

        return course, hole

    def get(self, request, **kwargs):
        course, hole = self.get_course_and_hole(kwargs)

        if not _auth_course(request.user, course):
            return HttpResponse('Access denied')

        form = HoleForm(instance=hole)

        tmpl_dict = {
            'hole': hole,
            'form': form,
            'course': course
        }

        return render(request, self.template_name, tmpl_dict)

    def post(self, request, **kwargs):
        course, hole = self.get_course_and_hole(kwargs)

        if not _auth_course(request.user, course):
            return HttpResponse('Access denied')

        form = HoleForm(request.POST, request.FILES,
            instance=hole)

        if form.is_valid():
            saved_hole = form.save()
            return HttpResponseRedirect(
                saved_hole.get_absolute_url())

        tmpl_dict = {
            'hole': hole,
            'form': form,
            'course': course
        }

        return render(request, self.template_name, tmpl_dict)


class HoleView(TemplateView):
    template_name = 'books/hole.html'

    def get(self, request, **kwargs):

        course_slug = kwargs.get('slug')
        position = kwargs.get('position')

        course = get_object_or_404(Course,
            slug=course_slug)

        hole = Hole.objects.get(course=course,
            position=position)

        can_edit = _auth_course(request.user, course)

        tmpl_dict = {
            'can_edit': can_edit,
            'MAPS_API_KEY': settings.MAPS_API_KEY,
            'hole': hole,
            'course': course,
        }

        return render(request, 'books/hole.html', tmpl_dict)


class CourseView(TemplateView):
    template_name = 'books/course.html'

    def get(self, request, **kwargs):
        course_slug = kwargs.get('slug')

        if kwargs.get('username'):
            user = get_object_or_404(User,
                username=kwargs.get('username'))

            course = get_object_or_404(Course,
                slug=course_slug, user=user)
        else:
            course = get_object_or_404(Course,
                slug=course_slug, active=True)

        holes = []

        for hole in course.hole_set.all():
            holes.append({
                'hole_position': hole.position,
                'hole_id': hole.id,
                'tee_pos': {
                    'lat': hole.tee_pos.latitude,
                    'lon': hole.tee_pos.longitude,
                },
                'basket_pos': {
                    'lat': hole.basket_pos.latitude,
                    'lon': hole.basket_pos.longitude,
                },
            })

        holes_json = simplejson.dumps(holes)

        return render(request, self.template_name, {
            'course':course, 'holes_json': holes_json,
            'MAPS_API_KEY': settings.MAPS_API_KEY})


class EditHoleGalleryView(View):
    template_name = 'books/hole/edit_gallery.html'

    def get(self, request, **kwargs):
        course, hole = self.get_course_and_hole(kwargs)

        if not _auth_course(request.user, course):
            return HttpResponse('Access denied')

        form = HoleGalleryImageForm()

        tmpl_dict = {
            'course': course,
            'form': form,
            'hole': hole,
            'can_edit': True,
        }

        return render(request, self.template_name, tmpl_dict)

    def post(self, request, **kwargs):
        course, hole = self.get_course_and_hole(kwargs)

        if not _auth_course(request.user, course):
            return HttpResponse('Access denied')

        form = HoleGalleryImageForm(request.POST, request.FILES)

        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.hole = hole
            new_image.save()

            return HttpResponseRedirect(
                hole.get_edit_gallery_url())

        tmpl_dict = {
            'course': course,
            'form': form,
            'hole': hole,
            'can_edit': True,
        }

        return render(request, self.template_name, tmpl_dict)

    def get_course_and_hole(self, args):
        course_slug = args.get('slug')
        hole_position = int(args.get('position'))

        course = get_object_or_404(Course, slug=course_slug)
        hole = get_object_or_404(Hole, course=course,
            position=hole_position)

        return course, hole


class EditHolePositionView(View):
    template_name = 'books/hole/edit_position.html'

    def get(self, request, **kwargs):
        course, hole = self.get_course_and_hole(kwargs)

        if not _auth_course(request.user, course):
            return HttpResponse('Access denied')

        form = HolePositionForm(instance=hole)

        tmpl_dict = {
            'course': course,
            'form': form,
            'hole': hole,
            'can_edit': True,
        }

        return render(request, self.template_name, tmpl_dict)

    def post(self, request, **kwargs):
        course, hole = self.get_course_and_hole(kwargs)

        if not _auth_course(request.user, course):
            return HttpResponse('Access denied')

        form = HolePositionForm(request.POST, request.FILES,
            instance=hole)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                hole.get_edit_position_url())

        tmpl_dict = {
            'course': course,
            'form': form,
            'hole': hole,
            'can_edit': True,
        }

        return render(request, self.template_name, tmpl_dict)

    def get_course_and_hole(self, args):
        course_slug = args.get('slug')
        hole_position = int(args.get('position'))

        course = get_object_or_404(Course, slug=course_slug)
        hole = get_object_or_404(Hole, course=course,
            position=hole_position)

        return course, hole
