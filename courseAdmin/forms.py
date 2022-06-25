from courses.models import Category, Course, CourseModule, Lesson, Quiz, CourseItem, Question, Choice
from django import forms


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = str(
                visible.field.label)
    class Meta:
        model = Category
        fields = ['title']



class CourseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = str(
                visible.field.label)
    class Meta:
        model = Course
        fields = ['title', 'short_description', 'description', 'outcome', 'prerequisite', 'language', 'price', 'category', 'thumbnail',]

class CourseModuleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CourseModuleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = str(
                visible.field.label)
    class Meta:
        model = CourseModule
        fields = '__all__'


class CourseItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CourseItemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = str(
                visible.field.label)
    class Meta:
        model = CourseItem
        fields = '__all__'

class LessonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = str(
                visible.field.label)
    class Meta:
        model = Lesson
        fields = ['title', 'duration', 'video_url', 'corres_course_item']


class QuizForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = str(
                visible.field.label)
    class Meta:
        model = Quiz
        fields = '__all__'


class QuestionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = str(
                visible.field.label)

    class Meta:
        model = Question 
        fields = '__all__'

class ChoiceForm(forms.ModelForm):


    class Meta:
        model = Choice 
        fields = '__all__'