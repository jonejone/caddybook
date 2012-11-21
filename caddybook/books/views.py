from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.context_processors import csrf

from caddybook.books.models import Course, Hole
from caddybook.books.forms import HoleForm, HoleGalleryImageForm, HolePositionForm

def index(request):
    courses = Course.objects.filter(active=True)

    return render(request, 'books/index.html', {
        'courses':courses})


def course(request, slug):
    course = get_object_or_404(Course,
        slug=slug, active=True)

    return render(request, 'books/course.html', {
        'course': course })


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
