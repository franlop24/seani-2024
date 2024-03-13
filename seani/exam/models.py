from django.db import models
from django.contrib.auth.models import User

from career.models import Career
from library.models import Module, Question

class Stage(models.Model):
    stage = models.IntegerField(
            verbose_name = "Etapa"    
        )
    application_date = models.DateField(
            verbose_name = "Fecha de Aplicación"    
        )
    
    @property
    def year(self):
        return self.application_date.year
    
    @property
    def month(self):
        months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        return months[self.application_date.month - 1]
    
    def __str__(self):
        return f"{ self.stage } - { self.month } { self.year }"
    
    class Meta:
        verbose_name = "etapa"
        verbose_name_plural = "etapas"

class Exam(models.Model):
    user = models.OneToOneField(
            User, 
            on_delete=models.CASCADE,
            verbose_name = "Usuario")
    career = models.ForeignKey(
            Career, 
            on_delete=models.CASCADE,
            verbose_name = "Carrera")
    stage = models.ForeignKey(
            Stage, 
            on_delete=models.CASCADE,
            verbose_name = "Etapa")
    score = models.FloatField(
            verbose_name = "Calificación",
            default = 0.0
        )
    modules = models.ManyToManyField(Module, through='ExamModule', verbose_name='Módulos')
    questions = models.ManyToManyField(Question, through='Breakdown')
    created = models.DateTimeField(
            verbose_name = "Fecha de creación",  
            auto_now_add=True)
    updated = models.DateTimeField(
            verbose_name = "Fecha de actualización",
            auto_now=True)
    
    def full_name(self):
        return f"{ self.user.last_name } { self.user.first_name }"

    def set_modules(self):
        for module in Module.objects.all():
            self.modules.add(module)
            #ExamModule.objects.create(exam=self, module=module)

    def set_questions(self):
        for module in self.modules.all():
            for question in module.question_set.all():
                Breakdown.objects.create(exam=self, question=question, correct=question.correct)

    def compute_score_by_module(self, module_id):
        score = 0.0
        for question in self.breakdown_set.filter(question__module_id=module_id):
            if question.correct == question.answer:
                score += 10.0
        exam_module = self.exammodule_set.get(module_id=module_id)
        exam_module.score = score / self.questions.filter(module_id=module_id).count()
        exam_module.active = False
        exam_module.save()

    def compute_score(self):
        score = 0.0
        for exam_module in self.exammodule_set.all():
            score += exam_module.score
        self.score = score / self.modules.count()
        self.save()

    def __str__(self):
        return f"{ self.user.username } - { self.score }"
    
    class Meta:
        verbose_name = "examen"
        verbose_name_plural = "examenes"

class ExamModule(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name = 'Módulo')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name = 'Examen')
    active = models.BooleanField(default=True, verbose_name = 'Activo')
    score = models.FloatField(default=0.0, verbose_name = 'Calificación')

    def __str__(self):
        return f"{ self.module.name }"
    
    class Meta:
        verbose_name = 'Módulo de Examen'
        verbose_name_plural = 'Módulos de Examen'

class Breakdown(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name = 'Examen')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name = 'Pregunta')
    answer = models.CharField(max_length=5, default = '-', verbose_name = 'Respuesta')
    correct = models.CharField(max_length=5, default = '-', verbose_name = 'Respuesta Correcta')

    def __str__(self):
        return f"{ self.question } { self.answer }"
    
class CustomExam(models.Model):
    class Meta:
        verbose_name = 'Agregar Aspirante'
        verbose_name_plural = 'Agregar Aspirantes'
        app_label = 'exam'

class LoadCSV(models.Model):
    class Meta:
        verbose_name = 'Cargar Aspirante'
        verbose_name_plural = 'Cargar Aspirantes'
        app_label = 'exam'