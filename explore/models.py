from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import IntegerField
from django.db.models.signals import post_save
from django.shortcuts import redirect
from django.utils import timezone
import requests
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    followers = models.IntegerField('followers',default=0)
    update_time = models.DateTimeField('update_time',null=True,blank=True)

class Repository(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    stars = models.IntegerField(default=0)

    class Meta:
        ordering = ['-stars']

def create_profile(sender,**kwargs):
    if kwargs['created']:
        username = kwargs['instance']
        flw = -1
        try:
            res = requests.get(f'https://api.github.com/users/{username}').json()
            flw = int(res['followers'])
        except Exception as err:
            print(err)
            redirect('/accounts/login')
        dt = timezone.now()
        user_profile = Profile.objects.create(user=username,followers=flw,update_time=dt)

def create_repo(sender,**kwargs):
    if kwargs['created']:
        profile_name = kwargs['instance']
        username = profile_name.user
        try:
            res = requests.get(f'https://api.github.com/users/{username}/repos').json()
            for i in res:
                repo = Repository.objects.create(profile=profile_name,stars=int(i['stargazers_count']),name=i['name'])
            
        except Exception as err:
            redirect('/accounts/login')
"""
def update(sender,**kwargs):
    req_user = kwargs['instance']
    user_prof = Profile.objects.filter(user=req_user)
    repos = Repository.objects.filter(profile=user_prof)
    #repos.delete()
    #try:
    
    res = requests.get(f'https://api.github.com/users/{req_user}').json()
    user_prof.followers = int(res['followers'])
    user_prof.update_time = timezone.now()
    user_prof.save()
    res_repo = requests.get(f'https://api.github.com/users/{req_user}/repos').json()
    for i in res_repo:
        repo = Repository.objects.create(profile=user_prof,stars=int(i['stargazers_count']),name=i['name'])
    print(request.user)
    return redirect(f'{request.user}')
"""
post_save.connect(create_profile,sender=User)
post_save.connect(create_repo,sender=Profile)
#post_save.connect(update,sender=User)