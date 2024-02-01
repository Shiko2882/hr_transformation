
# urls.py file
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .views import CustomLogoutView

urlpatterns = [
    path("", dashboard, name="home"),
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView, name='logout'),
    #Restriction Views
    path('admin/', admin_view, name='admin_view'),
    path('company/', company_view, name='company_view'),
    path('consultant/', consultant_view, name='consultant_view'),
    
    
    path('fill_inputs_form/<int:pk>/', fill_inputs_form, name='fill_inputs_form'),
    path('fill_evaluation_form/<int:pk>/', fill_evaluation_form, name='fill_evaluation_form_with_pk'),
    
    path('view_companies/', view_companies, name='view_companies'),
    path("createcompany/", createcompany, name="create_company"),
    path("updatecompany/<str:pk>", updatecompany, name="Update_Company"),
    path("companyprofile/<str:pk>", companyprofile, name="Company_Profile"),
    path('my-company-profile/', my_company_profile, name='my_company_profile'),
    
    path('view_consultants/', view_consultants, name='view_consultants'),
    path("createconsultant/", createconsultant, name="Create consultant"),
    path("updateconsultant/<str:pk>", updateconsultant, name="Update_consultant"),
    path("consultantprofile/<str:pk>", consultantprofile, name="Consultant Profile"),    

    path('attachments/<str:pk>', company_attachments, name='company_attachments'),
    path('attachment-widget/<str:pk>', attachment_widget, name='attachment_widget'),
    path('attachment/<int:attachment_id>/', attachment_detail, name='attachment_detail'),
    
    
    path('company/<str:pk>/assign_competencies/', assign_competencies, name='assign_competencies'),
    path('company/<str:pk>/', company_detail, name='company_detail'),
    path('company/<str:pk>/add_competency_record/', add_competency_record, name='add_competency_record'),

    path('add_user/', add_user, name='add_user'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('user_list/', user_list, name='user_list'),
    path('admin_password_change/<int:user_id>/', admin_password_change, name='admin_password_change'),
    path('profile/', profile, name='profile'),
    
    path('start_survey/<int:company_id>/', start_survey, name='start_survey'),
    path('survey_form/<int:company_id>/', survey_form, name='survey_form'),
   

] + static (settings.MEDIA_URL, document_root= settings.MEDIA_ROOT )
