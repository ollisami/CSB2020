from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import homeView, signUpView, gameView, answerView, highscoresView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='pages/login.html')),
    path('logout/', LogoutView.as_view(next_page='/')),
    path('signup/', signUpView, name='signup'),
    path('', homeView, name='home'),
    path('game/', gameView, name='game'),
    path('answer/', answerView, name='answer'),
    path('highscores/', highscoresView, name='highscores'),
]
