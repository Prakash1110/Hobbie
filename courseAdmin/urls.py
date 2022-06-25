from django.urls import path, include
from .views import *

urlpatterns =[
    path('', adminhome, name='admin-home'), # Shows all course for creator 
    path('cat/', categorysave, name='cat-save'), # for storing new category
    path('coursestore/', courseStore, name='course_save'), # For creating new course
    path('changeitems/<int:pk>/', itemChanges, name='item-delete'), # for deleting items i.e lesson or quiz
    path('updateitem/<int:pk>/', updateItem, name='item-update'), # For editing existing itmes 
    path('updatemodule/<int:pk>/', updateModule, name='module-update'), # For editing existing module 
    path('updatecourse/<slug:slug>/', updateCourse, name='course-update'), # For editing existing course
    path('coursechange/<slug:slug>/', courseChanges, name='course-update-and-delete'), # For deleting the course 
    path('coursemodulestore/<slug:slug>/', courseModuleStore, name='course-module-save'), # For creating new module 
    path('courseitems/<int:pk>/', itemView, name='item-view'), # Shows all items of module
    path('courseitemstore/lesson/<int:pk>/', courseLessonStore, name='course-lesson-save'), # For storing new lesson
    path('courseitemstore/quiz/<int:pk>/', courseQuizStore, name='course-quiz-save'), # For storing new quiz
    path('courseitem/quiz/questions/<int:pk>/', questionView, name='quiz-questions'), # For viewing quiz questions
    path('courseitem/quiz/questions/add/<int:pk>/', questionsStore, name='add-questions'), # For adding new questions to quiz
    path('courseitem/quiz/questions/edit/<int:pk>/', updateQuestion, name='question-edit'), # For editing questions
    path('courseitem/quiz/questions/del/<int:pk>/', questionDelete, name='question-delete'), # For deleting questions
    path('courseitem/quiz/choices/edit/<int:pk>/', updateChoice, name='choice-edit'), # For updating choices
    path('<slug:slug>/', modulesView, name='modules-view'), # For viewing all modules
    path('<slug:slug>/<int:pk>/', moduleChanges, name='module-delete'), # For deleting module 
]