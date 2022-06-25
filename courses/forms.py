from django.db.models import fields
from django.shortcuts import get_object_or_404
from .models import Question, QuizTaker, SelectedChoice, Quiz
from django import forms
from django.contrib.auth import get_user_model


class PlaceOrderForm(forms.Form):
    course_slug = forms.SlugField(widget=forms.HiddenInput(), required=False)
    total = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    
class QuizAttemptForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        self.quiz = kwargs.pop('quiz')
        self.question_set = kwargs.get('question_set')
        if self.question_set:
            kwargs.pop('question_set')
        super().__init__(*args, **kwargs)
        for q in self.question_set if self.question_set else self.quiz.question_set.all():
            self.fields[f'choices_question_{q.number}'] = forms.ModelChoiceField(
                queryset=q.choice_set.all(),
                required=False,
                widget=forms.RadioSelect(attrs={
                    'class': 'form-check-input'
                }
                )
            )


    def save(self):
        user = get_object_or_404(get_user_model(), id=self.user_id)
        quiztaker, q_iscreated = QuizTaker.objects.get_or_create(
            user=user, quiz=self.quiz, is_completed=True)
        if not q_iscreated:
            quiztaker.selectedchoice_set.all().delete()
        for q in self.quiz.question_set.all():
            if self.cleaned_data[f'choices_question_{q.number}']:

                SelectedChoice.objects.create(question=q,
                                              choice=self.cleaned_data[f'choices_question_{q.number}'],
                                              quiztaker=quiztaker
                                              )
        quiztaker.correct_answers_num = SelectedChoice.objects.filter(
            quiztaker=quiztaker,
            choice__is_correct=True).count()
        quiztaker.save()


class ChoiceForm(forms.ModelForm):
    choice = forms.ModelChoiceField(queryset=None, widget=forms.RadioSelect(
        attrs={
            'class': 'form-check-inline'
        }
    ))

    def __init__(self, *args, **kwargs):
        question_id = kwargs.pop('question_id', None)
        super().__init__(*args, **kwargs)
        self.fields['choice'].queryset = Question.objects.get(
            pk=question_id).choice_set.all()

    class Meta:
        model = SelectedChoice
        fields = ('choice',)


class QuizForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = str(
                visible.field.label)

    class Meta:
        model = Quiz
        fields = ('name', 'questions_count',
                  'description')


class ReattemptQuizForm(forms.Form):
    quiztaker_pk = forms.IntegerField(widget=forms.HiddenInput())


class ButtonForm(forms.Form):
    hidden_field = forms.CharField(
        widget=forms.HiddenInput(), required=False, initial='Submit')
