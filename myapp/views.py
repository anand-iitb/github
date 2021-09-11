from django.contrib.auth.forms import UserCreationForm
from myapp.forms import SignUpForm
from django.shortcuts import render,redirect
#from myapp.forms import SignUpForm
# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')
        else:
            return render(request, "signup.html", {'form':form })
    else:
        form = SignUpForm()

        args = {'form': form}
        return render(request,'signup.html',args)