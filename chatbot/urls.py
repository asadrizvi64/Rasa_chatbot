from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('update_nlu', NluApiView.as_view()),
    path('update_stories', StoryApiView.as_view()),
    path('update_domain', DomainApiView.as_view()),
    path("chat", ChatView.as_view(), name="chat_view"),
    path("chat_bot", ChatbotView.as_view()),
    path('train_command', RunRasaTrainCommandView.as_view()),
    path('run_rasa_server', RunRasaServerCommandView.as_view()),
    path('run_custom_actions', RunCustomActionCommandView.as_view()),
    path('terminate_rasa_server', TerminateRasaServerView.as_view()),
    path('get_policy_info', GetPolicyInfo.as_view()),
    path('api_call', ApiCall.as_view()),
]
