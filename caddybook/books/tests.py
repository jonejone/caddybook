from caddybook.books.models import Course, Hole


def generate_course(name, holes=18):
    course = Course.objects.create(
        name=name, active=True, slug=name.lower())

    for i in range(holes):
        n = i + 1
        name = 'Hole %i' % n

        Hole.objects.create(
            course=course, position=n, name=name)

    return course
