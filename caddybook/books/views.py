from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from caddybook.books.models import Course, Hole
from caddybook.books.forms import HoleForm

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
        'hole': hole })


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

    return render(request, 'books/hole_edit.html', {
        'hole': hole, 'form': form })
