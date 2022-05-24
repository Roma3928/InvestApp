from django import forms
from .models import User, Question, Answer
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator


tagsValidator = RegexValidator(r"[а-яА-Яa-zA-Z]",
                               "Tags should contain letters")


class SignUpForm(forms.ModelForm):
    repeat_password = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'repeat_password', 'password', 'avatar',)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('repeat_password')
        if not password == re_password:
            self.add_error('repeat_password', 'Passwords must match')


class SignInForm(forms.Form):
    password = forms.CharField()
    username = forms.CharField()

    def clean(self):
        super(SignInForm, self).clean()
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if not user:
            self.add_error('password', "Wrong username or password")


class NewQuestionForm(forms.ModelForm):
    tags = forms.CharField(validators=[tagsValidator])

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')


class AnswerForm(forms.Form):
    text = forms.CharField()

    class Meta:
        model = Answer
        fields = ('title', 'text')


