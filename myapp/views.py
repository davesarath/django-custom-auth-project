from django.shortcuts import render,HttpResponse,redirect
from .forms import UserChangeForm,UserCreationForm,UserUpdateForm,loginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import custm_user

def notLogined(fn):
    def warpper(request):
        if(request.user.is_authenticated):
            return redirect("home")
        else:
            return fn(request)
    return warpper

def handler404(request,a):
    print(a)
    return render(request, 'error404.html', status=404)

def handler500(request):
    print("a")
    return render(request, 'error500.html', status=500)

@notLogined
def auth_login(request):
    # if(request.user.is_authenticated):
    #     return redirect("home")
    if request.method=="POST":
        form=loginForm(request.POST)
        if form.is_valid():
            usr=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            login(request,usr)
            try:
                nxt=request.GET["next"]

            except:
                nxt="home"
            return redirect(nxt)
        else:
            return render(request,'account/login.html',{"form":form})

    else:
        form=loginForm()
        return render(request,'account/login.html',{"form":form})

@notLogined
def auth_reg(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login/")
        else:
            return render(request,'account/register.html',{"form":form})
    else:
        form=UserCreationForm()
        return render(request,'account/register.html',{"form":form})

@login_required(login_url="auth_login")
def home(request):
    return render(request,'home.html')

def auth_logout(request):
    logout(request)
    return redirect("/login/")

@login_required(login_url="auth_login")
def auth_update(request):
    if request.method=="POST":
        form=UserUpdateForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            return render(request,'account/profile_edit.html',{"form":form})
    else:
        form=UserUpdateForm(instance=request.user)
        return render(request,'account/profile_edit.html',{"form":form})

# def pro_picChange(request):
#     picInstane = propicmodel.objects.filter(user_id=request.user)
#     if picInstane:
#         picInstane=picInstane[0]
#         print(picInstane)
#     else:
#         picInstane=None
#     if request.method=="POST":
#         forms=proPicChangeForm(request.user,request.FILES,instance=picInstane)
#         print(request.FILES)
#         if(forms.is_valid()):
#             print("true")
#             forms.save()
#             return render(request,'account/profile_edit.html',{"form":forms})
#         else:
#             print("false")
#             return render(request,'account/profile_edit.html',{"form":forms})
#     else:

#         forms=proPicChangeForm(instance=picInstane)
#         return render(request,'account/profile_edit.html',{"form":forms})

@login_required(login_url="auth_login")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('home')
        else:
            args = {'form': form}
            return render(request, 'account/password_change_form.html', args)
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'account/password_change_form.html', args)
 

