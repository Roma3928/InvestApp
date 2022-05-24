from django.urls import path
from .views import *
from . import views
from .models import *

urlpatterns = [
    path('', views.index, name='home'),
    path('tax', views.taxCalculation, name='tax'),
    path('analytics', views.analytics, name='analytics'),

    path('form', FeedView.as_view(), name='main'),
    path('hot', HotQuestionsView.as_view(), name='hot'),
    path('ask', AskView.as_view(), name='ask'),
    path('question/<pk>', QuestionView.as_view(), name='question'),
    path('login', LogInView.as_view(), name="login"),
    path('signup', SignUpView.as_view(), name="signup"),
    path('signout', sign_out, name='signout'),
    path('profile/<pk>', ProfileView.as_view(), name='profile'),
    path('tag/<str:tag_name>', TagQuestionView.as_view(), name='tag'),
    path('question/<pk>/like', VotesView.as_view(model=Question, vote=LikeDislike.LIKE)),
    path('question/<pk>/dislike', VotesView.as_view(model=Question, vote=LikeDislike.DISLIKE)),
    path('answer/<pk>/like', VotesView.as_view(model=Answer, vote=LikeDislike.LIKE)),
    path('answer/<pk>/dislike', VotesView.as_view(model=Answer, vote=LikeDislike.DISLIKE)),
    path('question/<pk>/isliked', IsLikedView.as_view(model=Question)),
    path('answer/<pk>/isliked', IsLikedView.as_view(model=Answer)),
]
