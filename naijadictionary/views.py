from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from naijadictionary.models import Definition, UserProfile, Submited
from naijadictionary import forms
import difflib, random

#for login
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import CharField
from django.db.models.functions import Length
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import SingleObjectMixin



CharField.register_lookup(Length, 'length')
short = Definition.objects.filter(meaning__length__gt=25)
f_four = list(filter(lambda x: len(x)<11, short.values_list('word', flat=True)))
four = random.sample(f_four, 4)
t_four = random.sample(f_four, 24)



def index(request):
    form = forms.DefinitionForm()
    f_four = list(filter(lambda x: len(x)<8, Definition.objects.values_list('word', flat=True)))
    four = random.sample(f_four, 4)
    t_four = random.sample(f_four, 24)

    if request.method == "POST":
        form = forms.DefinitionForm(request.POST)
        
        if form.is_valid():
            ans = form.cleaned_data.get('word')
            try:
                defi = Definition.objects.get(word=ans)
            except ObjectDoesNotExist:
                ans = ans.lower() if ans.istitle() == True or ans.isupper() is True else ans.title()
                print("case changed")
                try:
                    defi = Definition.objects.get(word=ans)
                    print("change successful")
                    defi.meaning = defi.meaning.split(" | ") if " | " in defi.meaning else defi.meaning
                    return render(request, 'naijadict/sec.html', context={'defi':defi, 'form':form, 't_four':t_four})
                except ObjectDoesNotExist:
                    response = difflib.get_close_matches(ans,Definition.objects.values_list('word', flat=True))
                    if len(response) == 0:
                        return render(request, 'naijadict/invalid.html', context={'form':form, 'ans':ans, 't_four':t_four})
                    else:
                        defi = Definition.objects.get(word=response[0])
                        print(f"Initially searched word: {ans}\nAlternative gottend: {response[0]}")
                        defi.meaning = defi.meaning.split(" | ") if " | " in defi.meaning else defi.meaning
                        return render(request, 'naijadict/alt.html', context={'form':form, 'defi':defi, 'ans':ans, 't_four':t_four})
                
            
            print(f"{defi.word} was searched")
            print(f"{defi.word} means : {defi.meaning}")
            defi.meaning = defi.meaning.split(" | ") if " | " in defi.meaning else defi.meaning
            return render(request, 'naijadict/sec.html', context={'defi':defi, 'form':form, 't_four':t_four})

    return render(request, 'naijadict/index.html', context={'form':form, 'four':four})

def userreg(request):
    form = forms.UserInfoForm()
    otherform = forms.UserProfileInfoForm()
    registered = False
    newname = False

    if request.method == "POST":
        form = forms.UserInfoForm(data=request.POST)
        otherform = forms.UserProfileInfoForm(data=request.POST)

        if form.is_valid() and otherform.is_valid():
            newname = form.cleaned_data.get('first_name')
            # first of all deal with the usermodel form
            # save the form first then has the password
            
            # p0 = form.cleaned_data.get('password')
            # user.username = form.cleaned_data.get('username').lower()
            user = form.save()
            # p1 = user.password
            password = form.cleaned_data.get('password')
            # this next will hash the password saved into the database
            user.username = form.cleaned_data.get('username').lower()
            user.set_password(password)
            # pw = user.password
            # password now hashed, now save and over-write the initially saved normal password and replace with the hashedpassword
            user.save()
            # print(f"p0 = {p0}\n p1 = {p1}\n pw = {pw}")
            # now deal with the second form but dont commit yet means dont save immediately
            profile_form = otherform.save(commit=False)
            # now arrange a onetoone relationship by joining the two forms together to be saved as one
            profile_form.user = user

            # now check if picture is uploaded or any file
            if 'profile_pic' in request.FILES:
                profile_form.profile_pic = request.FILES['profile_pic']

            # now you can save it
            profile_form.save()

            registered = True

        # else:
        #     form = forms.UserInfoForm()
        #     otherform = forms.UserProfileInfoForm()
        #     print(form.errors, otherform.errors)
        #     return render(request, 'naijadict/register.html', context={'form': form, 'otherform':otherform, 'newname':newname, 'registered':registered})


    
    return render(request, 'naijadict/register.html', context={'form': form, 'otherform':otherform, 'newname':newname, 'registered':registered})





def userlogin(request): 
    invalidlogin = False
    
    
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            if user.is_active:
                login(request,user)
                messages.success(request, 'You have successfully logged in. WELCOME TO YOUR DASHBOARD')
                return HttpResponseRedirect(reverse('dashboard'))
                
            else:
                return HttpResponse("Sorry Your Account is not active")
        else:
            invalidlogin = 'OOPS! Your Username or Password is incorrect'
            print(f"{username} tried to login with {password}")
            return render(request, 'naijadict/login.html', context={'invalidlogin': invalidlogin})

    else:
        return render(request, 'naijadict/login.html')
    return render(request, 'naijadict/login.html')


@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


class WordsListView(ListView):
    paginate_by = 10
    CharField.register_lookup(Length, 'length')
    # queryset = Definition.objects.order_by('?')
    queryset = Definition.objects.filter(meaning__length__gt=25).order_by('?')
    template_name = 'naijadict/words.html'

    




# class UserDashList(LoginRequiredMixin, ListView):
#     paginate_by = 10
#     queryset = Submited.objects.filter(user_name=self.request.user)
#     template_name = 
#     def get_object(self, queryset=None):
#         return self.request.user


class WordDetailView(DetailView):
    # f_four = list(filter(lambda x: len(x)<11, Definition.objects.values_list('word', flat=True)))
    # four = random.sample(f_four, 4)
    # t_four = random.sample(f_four, 24)
    model = Definition
    template_name = 'naijadict/detail.html'
    slug_field = 'word'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.DefinitionForm()
        context['t_four'] = t_four
        return context



# @login_required
class UserDashboard(LoginRequiredMixin, DetailView):
    login_url = 'userlogin'
    model = User
    template_name = 'naijadict/dashboard.html'


    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub'] = Definition.objects.all()
        return context
    

class DefCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'userlogin'
    form_class = forms.SubmitedForm
    model = Submited
    template_name = 'naijadict/submitword.html'
    success_url = reverse_lazy('dashboard')
    success_message = "Thanks for your contribution, your word and definition will be uploaded as soon as it's reviewed"
    
    def form_valid(self, form):
        form.instance.post_user = self.request.user.userprofile
        return super().form_valid(form)

class DefUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    # form_class = forms.UserProfileInfoForm
    login_url = 'userlogin'
    fields = ('age', 'location')
    model = UserProfile
    template_name = 'naijadict/updateprofile.html'
    # success_url = reverse_lazy('dashboard')
    success_message = "Your profile was successfully updated"
    # slug_field = 'user.username'
    # slug_url_kwarg = 'user'
    
    

    