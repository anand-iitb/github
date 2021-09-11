from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import IntegerField
from django.db.models.signals import post_save
from django.shortcuts import redirect
from django.utils import timezone
import requests


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

post_save.connect(create_profile,sender=User)
post_save.connect(create_repo,sender=Profile)
