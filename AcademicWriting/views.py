import re

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.utils.timezone import now
from pip._vendor import requests

from AcademicWriting.forms import EssayCheckForm, AuthUserForm, WorkForm, TaskForm
from AcademicWriting.models import Articles, Task, Work
from AcademicWriting.models import Group as GP


class LoginView(LoginView):
    template_name = 'login_page.html'
    form_class = AuthUserForm
    success_url = 'profile'
    def get_success_url(self):
        return self.success_url


class Logout(LogoutView):
    next_page = reverse_lazy('articles')


class ArticlesListView(ListView):
    model = Articles
    template_name = 'articles.html'
    context_object_name = 'articles'


class ArticleDetailView(DetailView):
    model = Articles
    template_name = 'article_details.html'
    context_object_name = 'article'


def profile(request):
    if (not request.user.is_anonymous):
        context = {
        }
        template = 'profile_page.html'
        return render(request, template, context)
    else:
        return HttpResponseRedirect("login")


def tasks(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # form_results = TaskForm(request.POST)
            # new_task = form_results.save()
            # new_task.teacher = request.user
            # new_task.save()
            new_task = Task.objects.create()
            new_task.name = request.POST.get("name")
            new_task.deadline = request.POST.get("deadline")
            new_task.group = GP.objects.get(id=request.POST.get("group"))
            new_task.title = request.POST.get("title")
            new_task.paragraph_number = request.POST.get("paragraph_number")
            new_task.words_number = request.POST.get("words_number")
            new_task.teacher = request.user
            new_task.save()

        status = request.GET.get('status', 'all')
        if request.user.groups.all()[0].name == 'Students Group':
            task_list = Task.objects.filter(group=GP.objects.get(students=request.user))
        elif request.user.groups.all()[0].name == 'Teachers Group':
            task_list = Task.objects.filter(group=GP.objects.get(teachers=request.user))
        else:
            task_list = []
        if status == 'current':
            filtered_list = []
            for task in task_list:
                if now() < task.deadline:
                    filtered_list.append(task)
            task_list = filtered_list
        if status == 'finished':
            filtered_list = []
            for task in task_list:
                if now() >= task.deadline:
                    filtered_list.append(task)
            task_list = filtered_list
        context = {
            'tasks': task_list,
            'str': status,
            'is_teacher': request.user.groups.all()[0].name == 'Teachers Group',
            'form': TaskForm
        }
        template = 'tasks.html'
        return render(request, template, context)
    else:
        return HttpResponseRedirect("accounts/login")


def task_details(request, pk):
    if request.user.is_authenticated:
        status = request.GET.get('status', 'all')
        if request.user.groups.all()[0].name == 'Students Group':
            task = Task.objects.filter(group=GP.objects.get(students=request.user)).get(id=pk)
            work, is_created = Work.objects.get_or_create(task=task, student=request.user)
            if request.method == "POST":
                text = request.POST.get("text")
                work.text = text
                work.words_number = TextAnalysis.countWords(text)
                work.paragraph_number = TextAnalysis.countParagraphs(text)
                mistakes = TextAnalysis.findMistakes(text)
                work.mistakes_number = len(mistakes)
                mistakes_str = ''
                for mis in mistakes:
                    mistakes_str += mis + ', '
                work.mistakes = mistakes_str
                sp_words = TextAnalysis.findSpecialWords(text)
                work.specialwords_number = len(sp_words)
                sp_words_str = ''
                for word in sp_words:
                    sp_words_str += word + ', '
                work.specialwords = sp_words_str
                work.save()
            if is_created:
                form = WorkForm(initial={'text': 'Enter your text'})
            else:
                form = WorkForm(initial={'text': work.text})
            template = 'task_details.html'
            works_list = None

        elif request.user.groups.all()[0].name == 'Teachers Group':
            task = Task.objects.filter(group=GP.objects.get(teachers=request.user)).get(id=pk)
            template = 'task_details.html'
            if request.method == "POST":
                work_id = request.POST.get("id")
                result = request.POST.get("result")
                commentary = request.POST.get("commentary")
                work = Work.objects.get(id=work_id)
                work.result = result
                work.commentary = commentary
                work.save()
            work = None
            form = None
            works_list = Work.objects.filter(task=task)
        else:
            task = 'Task now found'
        context = {
            'task': task,
            'work_form': form,
            'work': work,
            'now': now(),
            'status': status,
            'is_student': request.user.groups.all()[0].name == 'Students Group',
            'is_teacher': request.user.groups.all()[0].name == 'Teachers Group',
            'works_list': works_list
        }
        return render(request, template, context)
    else:
        return HttpResponseRedirect("/accounts/login")



def checkEssay(request):
    if request.method == "POST":
        text = request.POST.get("text")
        wordsNumber = TextAnalysis.countWords(text)
        paragraphsNumber = TextAnalysis.countParagraphs(text)
        mistakes = TextAnalysis.findMistakes(text)
        percentage = int((len(mistakes)/wordsNumber*100))
        context = {
            "text": text.splitlines(),
            "words": wordsNumber,
            "paragraphs": paragraphsNumber,
            "spwords": '*TODO*',
            "mistakes": ', '.join(mistakes),
            "percentage": percentage
        }
        template = 'check_essay_result.html'
        return render(request, template, context)
    else:
        essayForm = EssayCheckForm()
        context = {
            "form": essayForm
        }
        template = 'check_essay.html'
        return render(request, template, context)


def home(request):
    context = {
    }
    template = 'base.html'
    return render(request, template, context)


class TextAnalysis:
    def deleteExtraSpaces(text):
        return re.sub(r'\s+', ' ', text)

    def countWords(text):
        return len(text.split())

    def countParagraphs(text):
        n = 0
        for line in text.splitlines():
            if line != '':
                n += 1
        return n

    def findMistakes(text):
        try:
            request = requests.get(
                'https://speller.yandex.net/services/spellservice.json/checkText',
                params={'text': text, 'options': 518}
            )
            return {mis['word'] for mis in request.json()}
        except:
            return {'Connection error'}

    def findSpecialWords(text):
        sp_words = {'to sum up', 'in addition', 'furthermore', 'as follows', 'for example', 'for instance', 'namely',
                    'apart from', 'besides', 'moreover', 'in conclusion', 'to summarize', 'finally'}
        result = set()
        lower_text = text.lower()
        for word in sp_words:
            if lower_text.find(word) != -1:
                result.add(word)
        return result
