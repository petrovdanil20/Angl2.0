from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms import DateTimeInput

from AcademicWriting.models import Work, Task


class EssayCheckForm(forms.Form):
    text = forms.CharField(label="Text", widget=forms.Textarea(attrs={'class': 'form-control'}))


class WorkForm(forms.Form):
    text = forms.CharField(label="Text", widget=forms.Textarea(attrs={'class': 'form-control'}))


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'deadline', 'group', 'title', 'paragraph_number', 'words_number')
        widgets = {
            'deadline': DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['deadline'].widget.attrs['type'] = 'datetime-local'


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
