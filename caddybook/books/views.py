from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.core.context_processors import csrf
from django.contrib.sites.models import get_current_site
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

import simplejson

from caddybook.books.models import Course, Hole
from caddybook.books.forms import HoleForm, HoleGalleryImageForm, HolePositionForm


class AboutView(TemplateView):
    template_name = 'books/about.html'


@login_required
def profile(request):
    tmpl_data = {
        'site': get_current_site(request),
    }
    return render(request, 'books/profile.html', tmpl_data)


def index(request):
    courses = Course.objects.filter(active=True)
    tmpl_data = {
        'courses': courses,
    }
    return render(request, 'books/index.html', tmpl_data)



def course(request, slug):
    course = get_object_or_404(Course,
        slug=slug, active=True)

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

    return render(request, 'books/course.html', {
        'course':course, 'holes_json': holes_json,
        'MAPS_API_KEY': settings.MAPS_API_KEY})


def hole(request, slug, position):
    course = get_object_or_404(Course,
        slug=slug, active=True)

    hole = Hole.objects.get(course=course,
        position=position)

    return render(request, 'books/hole.html', {
        'hole': hole, 'course': course,
        'MAPS_API_KEY': settings.MAPS_API_KEY,
        'CSRF': csrf(request)})


def hole_edit(request, slug, position):
    course = get_object_or_404(Course,
        slug=slug, active=True)

    hole = Hole.objects.get(course=course,
        position=position)

    if request.method == 'POST':
        form = HoleForm(request.POST, request.FILES,
            instance=hole)

        if form.is_valid():
            updated_hole = form.save()
            return HttpResponseRedirect(reverse(
                'books-hole', args=[hole.course.slug,
                hole.position]))
    else:
        form = HoleForm(instance=hole)

    return render(request, 'books/hole/edit.html', {
        'hole': hole, 'form': form, 'course': course })


def hole_edit_gallery(request, slug, position):
    course = get_object_or_404(Course,
        slug=slug, active=True)

    hole = Hole.objects.get(course=course,
        position=position)


    if request.method == 'POST':
        form = HoleGalleryImageForm(request.POST, request.FILES)

        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.hole = hole
            new_image.save()

            return HttpResponseRedirect(reverse(
                'books-hole-edit-gallery', args=[
                hole.course.slug,
                hole.position]))
    else:
        form = HoleGalleryImageForm()

    return render(request, 'books/hole/edit_gallery.html', {
        'hole': hole, 'form': form, 'course': course, })


def hole_edit_position(request, slug, position):
    course = get_object_or_404(Course,
        slug=slug, active=True)

    hole = Hole.objects.get(course=course,
        position=position)

    if request.method == 'POST':
        form = HolePositionForm(request.POST, request.FILES,
            instance=hole)

        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.hole = hole
            new_image.save()

            return HttpResponseRedirect(reverse(
                'books-hole-edit-position', args=[
                hole.course.slug,
                hole.position]))
    else:
        form = HolePositionForm(instance=hole)

    return render(request, 'books/hole/edit_position.html', {
        'hole': hole, 'form': form, 'course': course, })
