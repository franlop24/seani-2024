from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User
from .models import Exam

from .forms import CandidateForm
from django.http import HttpResponseRedirect

# Create your views here.
def create(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
    
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            stage = form.cleaned_data['stage']
            career = form.cleaned_data['career']
            
            user = User.objects.create_user(
                    username = email, 
                    password = password, 
                    email = email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            exam = Exam.objects.create(user = user, stage = stage, career = career)
            exam.set_modules()
            exam.set_questions()
            
            html = """<h1>Aspirante Guardado</h1>
            <a href="/exam/create/">Registrar otro</a>
            """
            return HttpResponse(html)
            # return HttpResponseRedirect("/thanks/")
    else:
        form = CandidateForm()
    return render(request, 'exam/create.html', { "form": form })