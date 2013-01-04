from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.sites.models import get_current_site
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from caddybook.books.models import Course
from caddybook.books.forms import CreateCourseForm


def _auth_course(user, course):
    auth = False

    if course.user == user or user.is_staff:
        auth = True

    return auth


def create_course(request):

    if not request.user.is_authenticated():
        tmpl_dict = {
            'site': get_current_site(request),
        }
        return render(
            request, 'books/account/create_course_nologin.html',
            tmpl_dict)

    if request.method == 'POST':
        form = CreateCourseForm(request.POST)

        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user

            course.slug = Course.slugify_unique(
                slugify(course.name))

            course.save()

            # Now that we have saved, we can create holes
            course.create_holes(
                int(form.cleaned_data.get('hole_count')))

            return HttpResponseRedirect(reverse(
                'books-user-course', args=[
                request.user.username, course.slug]))

    else:
        form = CreateCourseForm()

    tmpl_data = {
        'form': form,
        'site': get_current_site(request),
    }

    return render(
        request, 'books/account/create_course.html',
        tmpl_data)


@login_required
def profile(request):
    tmpl_data = {
        'site': get_current_site(request),
    }
    return render(request, 'books/profile.html', tmpl_data)


def index(request):
    courses = Course.objects.filter(
        active=True, published=True)

    tmpl_data = {
        'courses': courses,
    }
    return render(request, 'books/index.html', tmpl_data)
