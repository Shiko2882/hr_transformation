
# This is views.py file
from datetime import timezone
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .forms import AdminPasswordChangeForm
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from .models import Company, InputsCategory, InputsQuestion, InputsAnswer
from .forms import InputsAnswerForm
from .decorators import group_required



@group_required(groups=['Administrator'])
def admin_view(request):
    return render(request, 'user/permission/admin_view.html', {'user': request.user})

@group_required(groups=['Company'])
def company_view(request):
    return render(request, 'user/permission/company_view.html', {'user': request.user})

@group_required(groups=['Consultant'])
def consultant_view(request):
    return render(request, 'user/permission/consultant_view.html', {'user': request.user})




class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Welcome!')
        return response

@login_required
def CustomLogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('home')) 

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'user/profile.html', {'form': form})


def dashboard(request):
    companies = Company.objects.all() # Retrieve the first 6 companies
    consultants = Consultant.objects.all()  # Retrieve the first 6 consultants

    context = {"companies": companies, 'consultants': consultants}
    return render(request, 'home.html', context)

def company_attachments(request, pk):
    company = Company.objects.get(id=pk)
    form = AttachmentForm(request.POST or None, request.FILES or None)
    # Check if the company has any attachments
    attachments = company.company_attachments.all()
    if not attachments:
        messages.warning(request, "No attachments found for this company.")

    if request.method == 'POST' and form.is_valid():
        attachment = form.save(commit=False)
        attachment.company = company
        attachment.save()
        messages.success(request, "Attachment saved successfully!")
        return redirect('company_attachments', pk=pk)

    return render(request, 'company/company_attachments.html', {'company': company, 'attachments': attachments, 'form': form})

def attachment_widget(request, pk):
    company = Company.objects.get(pk=pk)
    attachments = company.company_attachments.all()
    if not attachments:
        messages.warning(request, "No attachments found for this company.")
    
    return render(request, 'company/attachment_widget.html', {'company': company, 'attachments': attachments})

def attachment_detail(request, attachment_id):
    attachment = get_object_or_404(Attachment, pk=attachment_id)
    return render(request, 'company/attachment_detail.html', {'attachment': attachment})



# views.py

def fill_inputs_form(request, pk=None):
    """
    Renders a form for filling inputs and saves the answers to the database.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int, optional): The primary key of the company. Defaults to None.

    Returns:
        HttpResponse: The HTTP response object.
    """
    try:
        company = Company.objects.get(id=pk, user=request.user)
    except Company.DoesNotExist:
        return HttpResponse('You are not assigned to this company.', status=403)
    categories = InputsCategory.objects.filter(InputsForm__company=company)
    questions = InputsQuestion.objects.all()
    questions_by_category = {}

    for category in categories:
        questions_by_category[category] = InputsQuestion.objects.filter(category=category)
            
    existing_answers = InputsAnswer.objects.filter(company=company).select_related('question')
    initial_data = {}

    for answer in existing_answers:
        initial_data[f'answer_{answer.question.id}'] = answer.answer
        initial_data[f'notes_{answer.question.id}'] = answer.notes

    if request.method == 'POST':
        form = InputsAnswerForm(request.POST, initial=initial_data)
        if form.is_valid():
            for question in questions:
                answer_field_name = f'answer_{question.id}'
                notes_field_name = f'notes_{question.id}'

                answer = form.cleaned_data.get(answer_field_name, 'N')
                notes = form.cleaned_data.get(notes_field_name, '')
                InputsAnswer.objects.update_or_create(
                    company=company,
                    question=question,
                    defaults={'answer': answer, 'notes': notes}
                )

            if 'submit' in request.POST:
                # Mark the records as submitted and make them not editable
                company.submitted = True
                company.save()
                messages.success(request, 'Data submitted successfully.')
            elif 'save_draft' in request.POST:
                messages.success(request, 'Data saved as draft.')
            return redirect('fill_inputs_form', pk=pk)
        else:
            # Form is not valid, handle errors or display them in the template
            pass
    else:
        form = InputsAnswerForm(initial=initial_data)

    return render(request, 'fill_inputs_form.html', {'form': form, 'questions': questions, 'company': company, 'pk': pk,  'questions_by_category': questions_by_category})





# create the view for evaluation answers form #


def fill_evaluation_form(request, pk=None):
    try:
        company = Company.objects.get(id=pk, user=request.user)
    except Company.DoesNotExist:
        return HttpResponse('You are not assigned to this company.', status=403)

    questions = EvaluationQuestion.objects.all()

    if request.method == 'POST':
        form = EvaluationAnswerForm(request.POST)
        if form.is_valid():
            for question in questions:
                answer_field_name = f'answer_{question.id}'
                notes_field_name = f'notes_{question.id}'

                answer = form.cleaned_data.get(answer_field_name, '')
                notes = form.cleaned_data.get(notes_field_name, '')

                defaults = {'answer': answer, 'notes': notes}
                if 'draft' in request.POST:
                    # save as draft
                    defaults['is_draft'] = True
                elif 'submit' in request.POST:
                    # submit
                    defaults['is_draft'] = False

                EvaluationAnswer.objects.update_or_create(
                    company=company,
                    question=question,
                    defaults=defaults
                )

            return HttpResponse('Thank you for your inputs')
    else:
        existing_answers = EvaluationAnswer.objects.filter(company=company)
        initial_data = {}
        for answer in existing_answers:
            answer_field_name = f'answer_{answer.question.id}'
            notes_field_name = f'notes_{answer.question.id}'
            initial_data[answer_field_name] = answer.answer
            initial_data[notes_field_name] = answer.notes

        form = EvaluationAnswerForm(initial=initial_data)

    return render(request, 'evaluation_answers_form.html', {'form': form, 'questions': questions, 'company': company, 'pk': pk})



# a view to view/create/update companies data #

def view_companies(request):
    companies = Company.objects.all()
    form = CompanyViewFormCreate()
    
    return render(request, 'company/view_companies.html', {'companies': companies , 'form': form})

def createcompany(request):
    form =CompanyViewFormCreate()
    if request.method == 'POST':
        form = CompanyViewFormCreate(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    
    context= {'form':form}
    return render(request,'company/company_create.html', context)

def updatecompany(request,pk):
    
    company = Company.objects.get(id=pk)
    form =CompanyViewFormUpdate(instance=company)
    if request.method == 'POST':
        form = CompanyViewFormUpdate(request.POST,instance=company)
        if form.is_valid():
            form.save()
            return redirect("/")
    
    context= {'form':form ,'company': company}
    return render(request,'company/companyform.html', context)


def companyprofile(request,pk):
    companyid= Company.objects.get(id=pk)
    attachments = companyid.company_attachments.all()
    competencies = companyid.company_attachments.all()
    competency_records = companyid.competency_records.all()
    available_competencies = companyid.competencies.all()
    form = CompetencyRecordForm(companyid)
    context = {"companyid":companyid, "attachments":attachments , "competencies":competencies , "competency_records":competency_records , "available_competencies":available_competencies} 
    return render(request, "company/companyprofile.html",context)

def my_company_profile(request):
    user = request.user
    company = Company.objects.filter(user=user).first()
    attachments = company.company_attachments.all()
    competencies = company.company_attachments.all()
    competency_records = company.competency_records.all()
    available_competencies = company.competencies.all()
    form = CompetencyRecordForm(company)
    context = {
        "company": company,
        "attachments": attachments,
        "competencies": competencies,
        "competency_records": competency_records,
        "available_competencies": available_competencies,
        "companyid":company
    }
    return render(request, "company/mycompanyprofile.html", context)
# a view to view/create/update consultants data #

def view_consultants(request):
    consultants = Consultant.objects.all()
    form = ConsultantViewForm()
    return render(request, 'consultant/view_consultant.html', {'consultants': consultants , 'form': form})

def createconsultant(request):
    form =ConsultantViewForm()
    if request.method == 'POST':
        form = ConsultantViewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    
    context= {'form':form}
    return render(request,'consultant/consultantform.html', context)

def updateconsultant(request, pk):
    consultant = Consultant.objects.get(user=pk)
    
    if request.method == 'POST':
        form = ConsultantViewForm(request.POST, instance=consultant)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = ConsultantViewForm(instance=consultant)
    
    context = {'form': form, 'consultantid': consultant}
    return render(request, 'consultant/consultantform.html', context)


def consultantprofile(request,pk):
    consultantid= Consultant.objects.get(user=pk)
    
    context = {"consultantid":consultantid }
    return render(request, "consultant/consultantprofile.html",context)

# Competencies Feature
def assign_competencies(request, pk):
    company = get_object_or_404(Company, pk=pk)
    assigned_competencies = company.competencies.all()
    available_competencies = Competency.objects.exclude(id__in=assigned_competencies.values_list('id', flat=True))

    if request.method == 'POST':
        selected_competencies = request.POST.getlist('competencies')
        company.competencies.add(*selected_competencies)  # Use add() instead of set() to append to the existing selection
        return redirect(request.path_info)  # Redirect to the same page

    return render(request, 'assign_competencies.html', {'companyid': company, 'available_competencies': available_competencies , 'assigned_competencies': assigned_competencies})

def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    competency_records = company.competency_records.all()

    return render(request, 'company_detail.html', {'companyid': company, 'competency_records': competency_records})

def add_competency_record(request, pk):
    company = get_object_or_404(Company, pk=pk)
    competency_records = company.competency_records.all()
    if request.method == 'POST':
        form = CompetencyRecordForm(company, request.POST)
        if form.is_valid():
            competency_record = form.save(commit=False)
            competency_record.company = company
            competency_record.save()
            return redirect(request.path_info)
    else:
        form = CompetencyRecordForm(company)

    return render(request, 'add_competency_record.html', {'form': form, 'companyid': company, 'pk': pk , 'competency_records': competency_records})


# a view to view/create/update users #

def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user.groups.set(form.cleaned_data['groups'])
            # If the user is assigned to the 'Consultant' group, create a new Consultant object
            if Group.objects.get(name='Consultant') in user.groups.all():
                Consultant.objects.create(user=user, created_at=timezone.now())
            return redirect('user_list')
    else:
        form = UserCreationForm()
    return render(request, 'user/add_user.html', {'form': form})



def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.groups.set(form.cleaned_data['groups'])
            return redirect('user_list')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'user/edit_user.html', {'form': form})



def user_list(request):
    users = User.objects.all()
    groups = Group.objects.all()
    
    return render(request, 'user/user_list.html', {'users': users, 'groups': groups})



def admin_password_change(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = AdminPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = AdminPasswordChangeForm(user)
    return render(request, 'user/admin_password_change.html', {'form': form})


@login_required
def company_form_view(request):
    # Get all questions and answers for the current user
    user_company = get_object_or_404(Company, user=request.user)
    questions = CompanyForm.objects.all()
    answers = CompanyFormAnswers.objects.filter(company=user_company )

    if request.method == 'POST':
        # Handle form submission
        for question in questions:
            answer_text = request.POST.get(f'answer_{question.id}', 'NA')
            notes_text = request.POST.get(f'notes_{question.id}', '')
            
            # Update or create CompanyFormAnswers
            answer, created = CompanyFormAnswers.objects.update_or_create(
                company=request.user,
                question=question,
                defaults={'answer': answer_text, 'notes': notes_text, 'is_draft': False}
            )

        messages.success(request, 'Form submitted successfully.')
        return redirect('company_form_view')

    return render(request, 'company_form_view.html', {'questions': questions, 'answers': answers })