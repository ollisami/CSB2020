from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from random import randrange
import sqlite3

from .models import Highscore, Secretassassin

# Create your views here.


def homeView(request):
    user = request.user
    request.session['level'] = 1
    request.session['points'] = 0
    return render(request, 'pages/home.html', {"user": user})


def signUpView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'pages/signup.html', {'form': form})

@login_required
def gameView(request):
    # Insert a secret assassin to secret table
    secret = Secretassassin(user=request.user, dateOfBirth=date.today(
    ), description='Super secret message no one should see.')
    secret.save()

    if request.method == 'POST':
        guess = request.POST.get("guess")
        request.session['guess'] = guess
        return redirect('/answer/')
    else:
        level = request.session.get('level', 0)
        if level >= 6:
            return redirect('/highscores/')
        return render(request, 'pages/game.html', {"level": level})

@login_required
def answerView(request):
    if request.method == 'POST':
        level = request.session.get('level', 0)
        request.session['level'] = level + 1
        return redirect('/game/')
    else:
        answer = randrange(10) + 1
        guess = request.session.get('guess', 0)
        points = request.session.get('points', 0)
        if str(answer) == guess:
            points += 5
        if str(answer - 1) == guess or str(answer + 1) == guess:
            points += 5
        request.session['points'] = points
        level = request.session.get('level', 0)
        return render(request, 'pages/answer.html', {"answer": answer, "guess": guess, "level": level, "points": points})

@login_required
def highscoresView(request):
    scoresLength = 0
    if request.method == 'POST':
        scoresLength = request.POST.get("scoresLength")
        print(scoresLength)

    points = request.session.get('points', 0)
    score = Highscore(player=request.user,
                      score=int(points), date=date.today())
    score.save()
    highscoresLength = request.session.get('length', 5)
    sql = "SELECT * FROM ( SELECT * FROM cybersecuritybase_highscore ORDER BY score ASC LIMIT '%s')" % (scoresLength)
    sqlhighscores = Highscore.objects.raw(sql)
    print(sqlhighscores)
    return render(request, 'pages/highscores.html', {'points': points, "highscores": sqlhighscores})
