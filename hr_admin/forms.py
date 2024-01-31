# This is forms.py file
from .models import *
from django.shortcuts import render,HttpResponse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import SetPasswordForm
from collections import defaultdict
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

# Form to handle the company data create#
class CompanyViewFormCreate(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        
# Form to handle the company data Update#
class CompanyViewFormUpdate(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__' 
        exclude = ['user', 'consultant', 'attachments','competencies','actionplanform','evaluationform','companyinputs','created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Update'))
        
# Form to handle the consultant data #
class ConsultantViewForm(forms.ModelForm):
    class Meta:
        model = Consultant
        fields = '__all__'
class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file', 'description']



class InputsAnswerForm(forms.ModelForm):
    YES_CHOICES = [
        ('NA', 'N/A'),
        ('Y', 'Yes'),
        ('N', 'No'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Group questions by category
        self.fields_by_category = defaultdict(list)
        categories = InputsCategory.objects.all()
        questions = InputsQuestion.objects.all().order_by('category')

        for question in questions:
            answer = f'answer_{question.id}'
            notes = f'notes_{question.id}'

            self.fields[answer] = forms.ChoiceField(
                label=question.name,
                choices=self.YES_CHOICES,
                required=False
            )
            self.fields[answer].category = question.category.name

            self.fields[notes] = forms.CharField(
                label=f'Notes',
                widget=forms.Textarea(attrs={'rows': 2}),
                required=False
            )
            self.fields[notes].category = question.category.name

            self.fields_by_category[question.category.name].append((answer, notes))

        # Crispy Forms layout configuration
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

        # Custom layout to organize fields
        self.helper.layout = Layout(
            # Add your layout configuration here based on your preferences
        )

    def clean(self):
        cleaned_data = super().clean()
        # Additional validation logic if needed
        return cleaned_data

    class Meta:
        model = InputsAnswer
        fields = ['answer', 'notes']



class EvaluationAnswerForm(forms.ModelForm):
    class Meta:
        model = EvaluationAnswer
        fields = ['answer', 'notes']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        questions = EvaluationQuestion.objects.all()

        for question in questions:
            answer = f'answer_{question.id}'
            notes = f'notes_{question.id}'

            self.fields[answer] = forms.CharField(
                label=question.name,
                required=False
            )

            self.fields[notes] = forms.CharField(
                label=f'Notes',
                widget=forms.Textarea(attrs={'rows': 8}),
                required=False
            )

    def clean(self):
        cleaned_data = super().clean()
        # Additional validation logic if needed
        return cleaned_data
    
class CompetencyRecordForm(forms.ModelForm):
    class Meta:
        model = CompetencyRecord
        fields = ['competency', 'date', 'achieved_number', 'notes']
        widgets = {
            'date': DateInput(format='%Y-%m-%d'),
        }

    def __init__(self, company, *args, **kwargs):
        super(CompetencyRecordForm, self).__init__(*args, **kwargs)
        self.fields['competency'].queryset = company.competencies.all()
    


# Form to handle adding new users

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'groups']

class UserUpdateForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups']



class AdminPasswordChangeForm(SetPasswordForm):
    old_password = None  # This disables the old password field

    class Meta:
        model = User
        fields = ('new_password1', 'new_password2',)