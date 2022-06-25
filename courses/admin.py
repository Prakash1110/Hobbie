from django.contrib import admin
from .models import Category, Course, CourseModule, Lesson, Question, Choice, CourseItem, SelectedChoice, Quiz, QuizTaker, Rating, EnrolledCourse,CourseOrder, Cart


class CourseAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Choice)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(QuizTaker)
admin.site.register(Rating)
admin.site.register(CourseItem)
admin.site.register(SelectedChoice)
admin.site.register(CourseModule)
admin.site.register(EnrolledCourse)
admin.site.register(CourseOrder)
admin.site.register(Cart)
