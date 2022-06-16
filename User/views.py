from django.shortcuts import render, redirect
# from django.contrib.auth.forms import RegisterForm
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
def register(request):
    if request.method== 'POST':
        form= RegisterForm(request.POST)
        if(form.is_valid()):
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!Please Login')
            form.save()
            return redirect('login')
    else:
        form= RegisterForm()
    return render(request, 'User/register.html', {'form': form})   
 
@login_required
def profile(request):
    return render(request, 'User/profile.html')

@login_required
def update(request):
    if request.method == 'POST':
        u_form= UserUpdateForm(request.POST,instance=request.user);
        p_form= ProfileUpdateForm(request.POST
                                  ,request.FILES
                                  ,instance=request.user.profile);
        if u_form.is_valid() and p_form.is_valid():
            u_form.save();
            p_form.save();
            messages.success(request,f'Account updated successfully!');
            return redirect('profile')
    else:
        u_form= UserUpdateForm(instance=request.user);
        p_form= ProfileUpdateForm(instance=request.user.profile);
    context= {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'User/profile_update.html',context);