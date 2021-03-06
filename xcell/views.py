from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import URLResolver, reverse_lazy
from django.urls import include
from django.urls import get_resolver

from api.models import *
from .forms import *
from django.contrib.auth import get_user_model
import myfitnesspal as mfp
User = get_user_model()


def Signup(request):
    if request.method == "POST":
        form = AddTrainerForm(request.POST)
        if form.is_valid():
            form.create()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = AddTrainerForm()
    return render(request, 'registration/signup.html', {'form': form})


def SignupClient(request, trainer=None):
    try:
        trainerUser = User.objects.get(username=trainer)
        trainer = Trainer.objects.get(trainer=trainerUser)
        username = trainerUser.username
        first_name = trainerUser.first_name
        last_name = trainerUser.last_name
    except:
        username = ''
        first_name = ''
        last_name = ''
    if request.method == "POST":
        form = AddClientForm(request.POST)

        if form.is_valid():

            print("form is valid")
            form.create()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=raw_password)
            trainer.clients.add(user)
            newWeek = Week(week=1,
                           phase=1,
                           user=user)
            newWeek.save()
            newPhase = Phase(phase=1, user=user)
            newPhase.save()
            newPhase.weeks.add(newWeek)
            newPhase.save()
            # // login(request, user)
            return redirect('success_client')
    else:
        form = AddClientForm()

    return render(request, 'registration/signup-client.html', {'form': form, 'username': username, 'first_name': first_name, 'last_name': last_name})


def Success(request):

    return render(request, 'registration/success.html')

def Mfp(request):
    user=User.objects.get(email=request.session[session_id+'_selected_client'])
    mfp_details = MyFitnessPal.objects.get(user=user)
    client = mfp.Client(mfp_details.username)
    vals= client.get_date(2022,4,19)
    print(vals)
    return render(request, 'registration/mfp.html',{"vals":vals})


# class LoginRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.login_url = settings.LOGIN_URL
#         self.open_urls = [self.login_url] + \
#             getattr(settings, 'OPEN_URLS', [])

#     def __call__(self, request):
#         if not request.user.is_authenticated \
#                 and not request.path_info in self.open_urls:
#             return redirect(self.login_url+'?next='+request.path)

#         return self.get_response(request)
