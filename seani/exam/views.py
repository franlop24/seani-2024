from django.shortcuts import render, redirect
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

def home(request):
    exam = request.user.exam
    modules = exam.exammodule_set.all()
    return render(request, 'exam/home.html', {'modules': modules} )

def module(request, module_id, question_id = 1):
    if request.method == 'GET':
        try:
            exam = request.user.exam
            questions = exam.questions.filter(module_id = module_id) 
            question = questions[question_id - 1]
            breakdown = exam.breakdown_set.filter(question__module_id = module_id)
            answer = breakdown[question_id - 1].answer
            return render(request, 'exam/question.html', {
                'question': question,
                'module_id': module_id,
                'question_id': question_id,
                'answer': answer,
                })
        except IndexError:
            return redirect('exam:home')
    if request.method == 'POST':
        exam = request.user.exam
        question = exam.breakdown_set.filter(question__module_id = module_id)[question_id - 1]
        answer = request.POST['answer']
        if question.answer != answer:
            question.answer = answer
            question.save()
        return redirect('exam:module', module_id, question_id + 1)

