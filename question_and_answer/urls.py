from django.urls import path
from . import views

urlpatterns = [
    path('save-ask/', views.QuestionCreateView.as_view, name='save_ask'),
]
