from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.core.context_processors import csrf
from django.contrib.sites.models import get_current_site
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.defaults import permission_denied
from django.utils.text import slugify

import simplejson

from caddybook.books.models import Course, Hole
from caddybook.books.forms import CreateCourseForm


class AboutView(TemplateView):
    template_name = 'books/about.html'


def _auth_course(user, course):
    auth = False

    if course.user == user or user.is_staff:
        auth = True

    return auth


@login_required
def create_course(request):

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
    }

    return render(request, 'books/account/create_course.html', tmpl_data)


@login_required
def profile(request):
    tmpl_data = {
        'site': get_current_site(request),
    }
    return render(request, 'books/profile.html', tmpl_data)


def index(request):
    courses = Course.objects.filter(active=True,
        published=True)

    tmpl_data = {
        'courses': courses,
    }
    return render(request, 'books/index.html', tmpl_data)
