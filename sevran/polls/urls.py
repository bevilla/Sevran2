from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:question_id>/', views.PollView.as_view(), name='poll'),
    path('<int:question_id>/vote/<int:choice_number>/', views.VoteView.as_view(), name='vote'),
]
