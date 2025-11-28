from django.urls import path
from .views import news_list
from .import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path("news/", news_list, name="news_list"),
]
