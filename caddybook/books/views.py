from django.shortcuts import render, get_object_or_404
from caddybook.books.models import Course, Hole

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
