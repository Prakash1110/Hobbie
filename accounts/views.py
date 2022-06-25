from courses.forms import QuizAttemptForm, ReattemptQuizForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.http.response import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_list_or_404, render, redirect, get_object_or_404
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, RedirectView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Category, CourseItem, CourseModule, Lesson, Course, Quiz, QuizTaker, Choice, SelectedChoice
from courses.models import EnrolledCourse
from .models import User
from .forms import ProfileUpdateForm, ApplicationForm
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings


class EnrolledCoursesListView(ListView):
    model = EnrolledCourse
    template_name = 'courses/enrolled_courses.html'
    context_object_name = 'enrolls'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('course').filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class StartCourseView(LoginRequiredMixin, DetailView):
    model = CourseItem
    template_name = 'lessons/lessons_by_course.html'
    context_object_name = 'lesson'


    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        course_module = course.modules.first()
        queryset = queryset.filter(course_module=course_module)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.first()
            if(hasattr(obj, 'lesson')):
                obj = obj.lesson
                url = obj.video_url
                url = url.replace("https://www.youtube.com/watch?v=",
                                  "https://www.youtube.com/embed/")
                obj.video_url = url
            else:
                raise queryset.model.DoesNotExist
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        context['course_modules'] = get_list_or_404(
            CourseModule, course=course)
        context["lessons"] = Lesson.objects.filter(
            corres_course_item__course_module__course=course)
        context["course"] = course
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "website/profile.html"
    context_object_name = "user"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("accounts:my-profile")

    def get_initial(self):
        return {"first_name": self.request.user.first_name, "last_name": self.request.user.last_name}

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.pk)




class LessonView(DetailView):
    model = Lesson
    template_name = 'lessons/lessons_by_course.html'
    context_object_name = 'lesson'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        lesson_id = self.kwargs['id']
        queryset = queryset.filter(id=lesson_id)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
            url = obj.video_url
            if 'watch' in url:
                url = url.replace("https://www.youtube.com/watch?v=",
                                  "https://www.youtube.com/embed/")
            else:
                url = url.replace("https://www.youtube.com/",
                                  "https://www.youtube.com/embed/")
            obj.video_url = url
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        context['course_modules'] = get_list_or_404(
            CourseModule, course=course)
        context["lessons"] = Lesson.objects.filter(
            corres_course_item__course_module__course=course)
        context["course"] = course
        return context

def apply_merchant(request):
    user=User
    if request.method =="POST":
        form=ApplicationForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"] 
            email = form.cleaned_data['email'],
            message = form.cleaned_data['message'],

            try:
                send_mail(subject, message, email, ['jettfury@gmail.com'], fail_silently=False,) 
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        return redirect ("accounts:my-profile")
    form = ApplicationForm()
    return render(request, "website/application_instructor.html", {
        'form':form,
        'user': user
        })

def apply_instructor(request):
    user=User
    if request.method =="POST":
        form=ApplicationForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            email= form.cleaned_data["email"] 
            body = {  
			'message':form.cleaned_data['message'], 
			}
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, email , ['jettfury@gmail.com'], fail_silently=False,) 
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        return redirect ("accounts:my-profile")
    form = ApplicationForm()
    return render(request, "website/application_instructor.html", {
        'form':form,
        'user': user
        })

def reattemptquiz(request):
    if request.POST and request.is_ajax:
        form = ReattemptQuizForm(request.POST)
        if form.is_valid():
            QuizTaker.objects.filter(
                user=request.user, pk=form.cleaned_data["quiztaker_pk"]).delete()
            return JsonResponse({
                'status': 'success',
            })
        else:
            print(form.errors)
    return HttpResponseForbidden()


def quiz_view(request, slug, quiz_id,):
    quiz = get_object_or_404(
        Quiz, id=quiz_id, corres_course_item__course_module__course__slug=slug)
    course = get_object_or_404(Course, slug=slug)

    if request.POST:
        form = QuizAttemptForm(request.POST, quiz=quiz,
                               user_id=request.user.id)
        if form.is_valid():
            form.save()
            return render(request, 'lessons/answers_by_quiz.html', {
                'quiztaker': QuizTaker.objects.get(user=request.user, quiz=quiz),
                'questions': quiz.question_set.all(),
                'quiz': quiz,
                'slug': slug
            })
    question_set = quiz.question_set.all().order_by('?')
    form = QuizAttemptForm(
        quiz=quiz, user_id=request.user.id, question_set=question_set)
    quiztaker_queryset = QuizTaker.objects.filter(
        user=request.user, quiz=quiz)
    if quiztaker_queryset.exists():
        quiztaker = quiztaker_queryset.first()
        reattempt_form = ReattemptQuizForm(
            initial={'quiztaker_pk': quiztaker.pk})
    else:
        reattempt_form = None
        quiztaker = None
    return render(request, 'lessons/quiz_by_course.html', context={
        'form': form,
        'questions': question_set,
        'course_modules': get_list_or_404(
            CourseModule, course=course),
        "lessons": Lesson.objects.filter(
            corres_course_item__course_module__course=course),
        "course": course,
        "reattempt_form": reattempt_form,
        'quiztaker': quiztaker
    })
