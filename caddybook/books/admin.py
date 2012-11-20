from django.contrib import admin
from caddybook.books.models import Course, Hole, HoleGalleryImage

class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name',) }


class HoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'position')


class HoleGalleryImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Course, CourseAdmin)
admin.site.register(Hole, HoleAdmin)
admin.site.register(HoleGalleryImage, HoleGalleryImageAdmin)
