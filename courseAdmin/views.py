from django.db.models.query import RawQuerySet
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth import get_user_model
User = get_user_model()
    
from courses.models import CourseModule, CourseItem, Lesson, Quiz
from .forms import *
# Create your views here.

def categorysave(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        title = request.POST.get('title')

        if form.is_valid():
            form.save()
        
        return redirect('/')   

    form = CategoryForm
    return render(request, 'courseAdmin/category.html', {'form' : form})

def courseChanges(request, slug):
    if request.method == 'POST':

        course = Course.objects.get(slug = slug)

        if course.user == request.user:
            course.delete()
            return JsonResponse({"status" : 200, "message" : "course deleted sucsessfully"})

        return JsonResponse({"status" : 405, "message" : "action not permitted"})
    
    return redirect(reverse_lazy('cat-save'))

def moduleChanges(request, pk, slug):
    if request.method == 'POST':
    
        course = Course.objects.get(slug = slug)
        module = CourseModule.objects.get(pk=pk, course=course)
    
        if course.user == request.user:
            module.delete()
            return JsonResponse({"status" : 200, "message" : "course module deleted sucsessfully"})

        return JsonResponse({"status" : 405, "message" : "action not permitted"})

    return redirect(reverse_lazy('admin-home'))


def itemChanges(request, pk):
    if request.method == 'POST':
    
        item = CourseItem.objects.get(pk=pk)
        module = item.course_module
        course = module.course
    
        if course.user == request.user:
            item.delete()
            return JsonResponse({"status" : 200, "message" : "course item deleted sucsessfully"})

        return JsonResponse({"status" : 405, "message" : "action not permitted"})

    return redirect(reverse_lazy('cat-save'))

def questionDelete(request, pk):
    if request.method == 'POST':
        question = Question.objects.get(pk=pk)

        course = question.quiz.corres_course_item.course_module.course
        if request.user == course.user:
            question.delete()
            return JsonResponse({"status" : 200, "message" : "course item deleted sucsessfully"})

        return JsonResponse({"status" : 405, "message" : "action not permitted"})
    
    return redirect(reverse_lazy('cat-save'))
    
def updateQuestion(request, pk):
    if request.method == "POST":
        question = Question.objects.get(pk=pk)
        quiz = question.quiz
        label = request.POST.get('label') or question.label
        number = request.POST.get('number') or question.number
        form = QuestionForm(dict(label=label, number=number, quiz=quiz), instance=question)
        
        if form.is_valid():
            form.save()
            return JsonResponse({"status" : 200, "message" : "question updated"})
    
    return JsonResponse({"status" : 405, "message" : "not updated"})

def updateChoice(request, pk):
    if request.method == 'POST':
        
        choice = Choice.objects.get(pk=pk)
        question = choice.question
        text = request.POST.get('text')
        is_correct = request.POST.get('is_correct')
        
        form = ChoiceForm(dict(question=question, text=text, is_correct=is_correct), instance=choice)
        
        if form.is_valid():
            form.save()
            return JsonResponse({"status" : 200, "message" : "Option updated"})


    return JsonResponse({"status" : 405, "message" : "not updated"})


def updateCourse(request, slug):
    course = get_object_or_404(Course, slug=slug)
    form = CourseForm(request.POST or None, instance=course)
    
    if form.is_valid():
        form.save()
        if request.method == 'POST':
            return redirect(reverse_lazy('admin-home'))

    return render(request, 'courseAdmin/updateCourse.html', {'form' : form, 'slug':slug})

def updateModule(request, pk):

    module = get_object_or_404(CourseModule, pk=pk)
    
    course = module.course
    slug = course.slug
    form = CourseModuleForm(request.POST or None, instance=module)
    if form.is_valid():
        form.save()
        if request.method == 'POST':
            return redirect(reverse_lazy('modules-view', args=[slug]))
    
    return render(request, 'courseAdmin/updateModule.html', {'form' : form, 'pk' : pk})

def updateItem(request, pk):
    item = get_object_or_404(CourseItem, pk=pk)
    mod_pk = item.course_module.pk
    if item.type == 'LS':
        lesson = get_object_or_404(Lesson, corres_course_item=item)
        form = LessonForm(request.POST or None, instance=lesson)
        if form.is_valid():
            form.save()
            if request.method=='POST':
                return redirect(reverse_lazy('item-view', args=[mod_pk]))
    else:
        quiz = get_object_or_404(Quiz, corres_course_item=item)
        form = QuizForm(request.POST or None, instance=quiz)
        if form.is_valid():
            form.save()
            if request.method=='POST':
                return redirect(reverse_lazy('item-view', args=[mod_pk]))
    
    return render(request, 'courseAdmin/updateItems.html', {'form' : form, 'pk':pk})

def questionView(request, pk):
    quiz = Quiz.objects.get(pk = pk)
    questions = Question.objects.filter(quiz=quiz)
    choices = []
    for question in questions:
        choice = Choice.objects.filter(question=question)
        choices.append(choice)
    params = zip(questions, choices)
    return render(request, 'courseAdmin/questionview.html', {'params' : params, 'pk':pk})

# @login_required(login_url=reverse_lazy('accounts:signin'))
def courseStore(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            slug = course.slug
            return redirect(reverse_lazy('course-module-save', args = [slug]))
    else:
        form = CourseForm
    return render(request, 'courseAdmin/course.html', {'form' : form})    

def courseModuleStore(request, slug):
    '''
        For creating new module along with its item.
        We pass slug of course whose modules and items need to be created.
    '''
    if request.method == 'POST':

        course = Course.objects.get(slug=slug)
        serial = request.POST.get('serial')
        module_name = request.POST.get('module-name')
        form = CourseModuleForm(dict(serial_num=serial, name=module_name, course=course))

        if form.is_valid():
            course_module = form.save()

        # Collecting data from request 

        course_item_nums_lesson = request.POST.getlist('course-item-num-lesson')
        lesson_names = request.POST.getlist('lesson-title')
        lesson_durations = request.POST.getlist('lesson-duration')
        lesson_urls = request.POST.getlist('lesson-url')
        course_item_nums_quiz = request.POST.getlist('course-item-num-quiz')
        quiz_titles = request.POST.getlist('quiz-title')
        question_counts = request.POST.getlist('question-count')
        quiz_description = request.POST.getlist('quiz-description')
        question_nums = request.POST.getlist('question-num')
        question_description = request.POST.getlist('question-description')
        options_1 = request.POST.getlist('option-1')
        options_2 = request.POST.getlist('option-2')
        options_3 = request.POST.getlist('option-3')
        options_4 = request.POST.getlist('option-4')
        correct_choices = request.POST.getlist('correct-choice')



        # lesson creation

        course_lesson_item_forms = [
            CourseItemForm(dict(serial_num = n, course_module = course_module, type='LS'))for n in course_item_nums_lesson
        ]
        cleaned_course_lesson_item_forms = []
        for form1 in course_lesson_item_forms:
            if form1.is_valid():
                a = form1.save() 
                cleaned_course_lesson_item_forms.append(a)

        forms = [
            LessonForm(dict(title=title, duration=dur, video_url=url, corres_course_item  = item))
            for title, dur, url, item in zip(
                lesson_names,
                lesson_durations,
                lesson_urls,
                cleaned_course_lesson_item_forms,
            )
        ]
        lessons = []
                   
        for form in forms:
            if form.is_valid():
                l = form.save()
                lessons.append(l)
            else:
                print(form)

        # Quiz creation
        
        course_quiz_item_forms = [
            CourseItemForm(dict(serial_num = n, course_module = course_module, type='QZ'))for n in course_item_nums_quiz
        ]
        
        cleaned_course_quiz_item_forms = []
        for form1 in course_quiz_item_forms:
            if form1.is_valid():
                a = form1.save() 
                cleaned_course_quiz_item_forms.append(a)
        

        forms_quizzes = [
            QuizForm(dict(name=title, questions_count=count, description=des, corres_course_item  = item))
            for title, count, des, item in zip(
                quiz_titles,
                question_counts,
                quiz_description,
                cleaned_course_quiz_item_forms,
            )
        ]
        quizzes = []
                   
        for form in forms_quizzes:
            if form.is_valid():
                q = form.save()
                quizzes.append(q)
            else:
                print(form)
        

        questions = []
        for q in quizzes:
            count = q.questions_count
            for i in range(len(questions),count):
                questions.append(QuestionForm(dict(number=question_nums[i], label=question_description[i], quiz = q)))
        created_questions = []
        for q_form in questions:
            if q_form.is_valid():
                q = q_form.save()
                created_questions.append(q)
            else:
                print(q_form)
        
        choices = []
        for q, opt1, opt2, opt3, opt4, cc in zip(created_questions, options_1, options_2, options_3, options_4, correct_choices):
            options = [opt1, opt2, opt3, opt4]

            for i in range (0,4): 
                if i == ord(cc)-97:
                    choices.append(ChoiceForm(dict(question=q, text=options[i], is_correct=True)))
                else:
                    choices.append(ChoiceForm(dict(question=q, text=options[i])))


        for choice_form in choices:
            if choice_form.is_valid():
                choice_form.save()
            else:
                print(choice_form)


        return redirect(reverse_lazy('item-view', args = [course_module.pk]))

    return render(request, 'courseAdmin/courseModule.html', {'slug' : slug})
    
def courseLessonStore(request, pk):
    if request.method == 'POST':
        module = CourseModule.objects.get(pk=pk)
        serial_num = request.POST.get('serial_num')
        item = CourseItemForm(dict(serial_num=serial_num, course_module = module, type = 'LS'))
        if item.is_valid():
            item = item.save()
            data = dict(request.POST)
            data['corres_course_item'] = item
            data['serial_num'] = data['serial_num'][0] 
            data['title'] = data['title'][0] 
            data['duration'] = data['duration'][0] 
            data['video_url'] = data['video_url'][0] 
            form = LessonForm(data)
            if form.is_valid():
                print(form.cleaned_data)
                form = form.save(commit=False)
                form.save()
            else:
                print(form) 
        return redirect(reverse_lazy('item-view', args=[pk]))        
    else:
        form = CourseItemForm
    return render(request, 'courseAdmin/courseLessonStore.html', {'form' : form})

def courseQuizStore(request, pk):
    if request.method == 'POST':
        print(request.POST)
        data = dict(request.POST)
        module = CourseModule.objects.get(pk=pk)
        serial_num = request.POST.get('serial_num')
        item = CourseItemForm(dict(serial_num=serial_num, course_module = module, type = 'QZ'))
        if item.is_valid():
            item = item.save()
            data['corres_course_item'] = item
            data['name'] = data['name'][0] 
            data['description'] = data['description'][0] 
            data['questions_count'] = data['questions_count'][0] 
            form = QuizForm(data)
            if form.is_valid():
                print(form.cleaned_data)
                quiz = form.save()
            else:
                print(form)
        
        # DATA COLLECTION

        question_num = request.POST.getlist('question-num')
        question_description = request.POST.getlist('question-description')
        options_1 = request.POST.getlist('option-1')
        options_2 = request.POST.getlist('option-2')
        options_3 = request.POST.getlist('option-3')
        options_4 = request.POST.getlist('option-4')
        correct_choices = request.POST.getlist('correct-choice')

        questions_forms = [
            QuestionForm(dict(number = num, label = label, quiz = quiz))
            for num, label in zip(question_num, question_description)
        ]
        created_questions = []
        for q in questions_forms:
            if q.is_valid():
                ques = q.save()
                created_questions.append(ques)
            else:
                print(q)     

        choices = []
        for q, opt1, opt2, opt3, opt4, cc in zip(created_questions, options_1, options_2, options_3, options_4, correct_choices):
            options = [opt1, opt2, opt3, opt4]

            for i in range (0,4): 
                if i == ord(cc)-97:
                    choices.append(ChoiceForm(dict(question=q, text=options[i], is_correct=True)))
                else:
                    choices.append(ChoiceForm(dict(question=q, text=options[i])))


        for choice_form in choices:
            if choice_form.is_valid():
                choice_form.save()
            else:
                print(choice_form)

        return redirect(reverse_lazy('item-view', args=[pk]))        
    else:
        form = QuizForm()
    return render(request, 'courseAdmin/quizstore.html', {'form' : form})

def questionsStore(request, pk):
    if request.method=='POST':
        quiz = Quiz.objects.get(pk=pk)
        question_num = request.POST.getlist('question-num')
        question_description = request.POST.getlist('question-description')
        options_1 = request.POST.getlist('option-1')
        options_2 = request.POST.getlist('option-2')
        options_3 = request.POST.getlist('option-3')
        options_4 = request.POST.getlist('option-4')
        correct_choices = request.POST.getlist('correct-choice')

        questions_forms = [
            QuestionForm(dict(number = num, label = label, quiz = quiz))
            for num, label in zip(question_num, question_description)
        ]
        created_questions = []
        for q in questions_forms:
            if q.is_valid():
                ques = q.save()
                created_questions.append(ques)
            else:
                print(q)     

        choices = []
        for q, opt1, opt2, opt3, opt4, cc in zip(created_questions, options_1, options_2, options_3, options_4, correct_choices):
            options = [opt1, opt2, opt3, opt4]

            for i in range (0,4): 
                if i == ord(cc)-97:
                    choices.append(ChoiceForm(dict(question=q, text=options[i], is_correct=True)))
                else:
                    choices.append(ChoiceForm(dict(question=q, text=options[i])))


        for choice_form in choices:
            if choice_form.is_valid():
                choice_form.save()
            else:
                print(choice_form)

        return redirect(reverse_lazy('quiz-questions', args=[pk]))

    return render(request, 'courseAdmin/addquestion.html', {'pk':pk})

def adminhome(request):
    courses = Course.objects.all()
    return render(request, 'courseAdmin/dashboard.html', {'courses' : courses})


def modulesView(request, slug):
    course = Course.objects.get(slug = slug)
    try:
        course_modules = CourseModule.objects.filter(course=course)
    except CourseModule.DoesNotExist:
        course_modules = []

    return render(request, 'courseAdmin/moduleview.html', {'course_modules' : course_modules, 'slug' : slug})

def itemView(request, pk):
    course_module = CourseModule.objects.get(pk = pk)
    course_items = CourseItem.objects.filter(course_module=course_module)
    items = []
    for item in course_items:
        it = []
        it.append(item)
        if item.type == 'LS':
            try:
                it.append(Lesson.objects.get(corres_course_item=item))
            except Lesson.DoesNotExist:
                it.pop()
        else:
            try:
                it.append(Quiz.objects.get(corres_course_item=item))
            except Quiz.DoesNotExist:
                it.pop()
        
        
        if it.__len__ != 0:
            items.append(it)

    return render(request, 'courseAdmin/lessonView.html', {'items' : items, 'pk' : pk})


