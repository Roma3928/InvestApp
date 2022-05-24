from django.http import HttpResponse
from django.views.generic import ListView, DetailView, UpdateView, View
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate,login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from annoying.functions import get_object_or_None
from django.http import JsonResponse
from .models import *
from .forms import *

def index(request):
    content = News.objects.all()
    context = {
        'content': content,
    }
    return render(request, 'main/index.html', context=context)


def taxCalculation(request):
    c = ''
    try:
        if request.method == "POST":
            n1 = eval(request.POST.get('pr'))
            n2 = eval(request.POST.get('kpr'))
            n3 = eval(request.POST.get('po'))
            n4 = eval(request.POST.get('kpo'))
            opr = request.POST.get('opr')
            if opr == "dividends":
                i = (n1 - n2 - n3 - n4) * 0.13
                c = int(i + (0.5 if i > 0 else -0.5))
            elif opr == "currency":
                i = (n1-n2-n3-n4)*0.13
                c = int(i + (0.5 if i > 0 else -0.5))
            elif opr == "metal":
                i = (n1 - n2 - n3 - n4) * 0.13
                c = int(i + (0.5 if i > 0 else -0.5))
    except:
        c = 'Некорректный ввод'
    print(c)
    return render(request, 'main/tax.html', {'c': c})


def analytics(request):
    return render(request, 'main/analytics.html')


class FeedView(ListView):
    paginate_by = 6
    model = Question
    ordering = ["-date"]
    template_name = "main/feed.html"


class QuestionView(DetailView):
    model = Question
    template_name = "main/question.html"
    form_class = AnswerForm

    def get_context_data(self, **kwargs):
        return super(QuestionView, self).get_context_data(form=self.form_class, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.object = self.get_object()
        context = self.get_context_data()
        form = self.form_class(request.POST)
        if form.is_valid():
            Answer.objects.create(author=request.user,
                                  text=form.cleaned_data['text'],
                                  question=self.object)
            return self.render_to_response(context)
        else:
            context['form'] = form
            return self.render_to_response(context)


class HotQuestionsView(ListView):
    paginate_by = 6
    model = Question
    ordering = ["-rate"]
    template_name = "main/feed.html"


class TagQuestionView(ListView):
    paginate_by = 6
    template_name = "main/tag_questions.html"
    context_object_name = "questions"

    def get_context_data(self, **kwargs):
        kwargs["tag"] = self.kwargs["tag_name"]
        return super(TagQuestionView, self).get_context_data(**kwargs)

    def get_queryset(self):
        return Tag.objects.questions_by_tag(self.kwargs['tag_name'])


class AskView(LoginRequiredMixin, FormView):
    form_class = NewQuestionForm
    template_name = 'main/ask.html'
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            question = Question.objects.create(author=request.user,
                                               title=form.cleaned_data['title'],
                                               text=form.cleaned_data['text'])
            form.cleaned_data['tags'].strip()
            for tagTitle in form.cleaned_data['tags'].split():
                tag = Tag.objects.get_or_create(title=tagTitle)[0]
                question.tags.add(tag)
                question.save()
            return HttpResponseRedirect(reverse('question', args=[question.pk]))
        else:
            return self.form_invalid(form)


@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect('/')


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = "main/signup.html"
    success_url = '/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        return redirect(self.success_url)


class LogInView(FormView):
    form_class = SignInForm
    template_name = "main/login.html"
    success_url = '/'

    def form_valid(self, form):
        print(self.get_form_kwargs())
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        login(self.request, user)
        return redirect(self.success_url)


def profile(request):
    return render(request, "main/user_profile.html", {})


class ProfileView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    fields = ('username', 'email', 'avatar')
    model = User
    template_name = 'main/user_profile.html'
    success_url = '../'


class VotesView(LoginRequiredMixin, View):
    login_url = 'login'
    model = None
    vote = None

    def post(self, request, pk):
        color = None
        if self.vote == LikeDislike.LIKE:
            color = 'green'
        else:
            color = 'red'
        obj = self.model.objects.get(pk=pk)
        vote_obj = get_object_or_None(LikeDislike, content_type=ContentType.objects.get_for_model(obj),
                                      object_id=pk,
                                      user=request.user)
        if not vote_obj:
            new = LikeDislike(vote=self.vote, user=request.user,
                              content_object=obj)
            new.save()
            new.content_object.rate += self.vote
            new.content_object.save()

            return JsonResponse({'rate': new.content_object.rate, 'color': color})
        if vote_obj.vote == self.vote:
            return JsonResponse({'rate': vote_obj.content_object.rate, 'color': color})
        else:
            vote_obj.delete()
            return JsonResponse({'rate': vote_obj.content_object.rate, 'color': 'black'})


class IsLikedView(LoginRequiredMixin, View):
    login_url = 'login'
    model = None

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        vote_obj = get_object_or_None(LikeDislike, content_type=ContentType.objects.get_for_model(obj),
                                      object_id=pk,
                                      user=request.user)
        if not vote_obj:
            return JsonResponse({'isliked': 0})
        if vote_obj.vote == 1:
            return JsonResponse({'isliked': 1})
        else:
            return JsonResponse({'isliked': -1})
