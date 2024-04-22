from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("feedback/", views.index, name='feedback'),
    path("about/", views.about, name='about'),
    path("chatbot/", views.chatbot, name='chatbot'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path("services/", views.services, name='services'),
    path("checker/", views.checker, name='checker'),
    path("quiz/", views.quiz, name='quiz'),
    path('word/', views.word, name='word'),
    path("synonyms_antonyms/", views.synonyms_antonyms, name='synonyms_antonyms'),
]
