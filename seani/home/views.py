from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin:index')
        else:
            return redirect('exam:home')
    return render(request, 'home/home.html')