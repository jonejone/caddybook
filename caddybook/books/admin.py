from django.contrib import admin
from caddybook.books.models import Course, Hole

class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name',) }


class HoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'position')


admin.site.register(Course, CourseAdmin)
admin.site.register(Hole, HoleAdmin)
