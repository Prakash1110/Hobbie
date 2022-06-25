from django.urls import path, include

from . import views

app_name = 'accounts'

urlpatterns = [
    path('users/', include([
         path('my-courses/', views.EnrolledCoursesListView.as_view(),
              name='enrolled-courses'),
         path('my-courses/<slug:slug>/view/',
              views.StartCourseView.as_view(), name='course-lessons'),
         path('my-courses/<slug:slug>/lessons/<int:id>/',
              views.LessonView.as_view(), name='course-lessons-single'),
         path('my-courses/<slug:slug>/quiz/<int:quiz_id>/',
              views.quiz_view, name='quiz_view'),
         path('my-courses/reattempt-quiz/',
              views.reattemptquiz, name='reattempt-quiz'),
         path('profile/', views.ProfileUpdateView.as_view(), name='my-profile'),
         path('apply_instructor/', views.apply_instructor, name='instructor'),
         ])),
]
