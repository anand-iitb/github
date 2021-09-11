from explore.models import Profile, Repository
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.utils import timezone
import requests
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def explore(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    all_entries = User.objects.all()
    return render(request,'explore.html',{'entries': all_entries})

@cache_control(no_cache=True, must_revalidate=True,  no_store=True)
def profile(request,user_name):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    person = User.objects.filter(username=user_name)
    prof = Profile.objects.filter(user=person.first())
    repos = Repository.objects.filter(profile=prof.first())
    return render(request,'profile.html',{'person':person.first(),'profile':prof.first,'repos':repos})

def update_prof(request):
    user_prof = Profile.objects.get(user=request.user)
    repos = Repository.objects.filter(profile=user_prof)
    try:
        user_prof.update_time = timezone.now()
        res = requests.get(f'https://api.github.com/users/{request.user}').json()
        user_prof.followers = int(res['followers'])
        user_prof.save()
        res_repo = requests.get(f'https://api.github.com/users/{request.user}/repos').json()
        repos.delete()
        for i in res_repo:
            repo = Repository.objects.create(profile=user_prof,stars=int(i['stargazers_count']),name=i['name'])
    except Exception as err:
        print("done")

    return redirect(f'/explore/{request.user}')
