"""
URL configuration for hr_database project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hr_app import views
from config import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    path('addEmployee/', views.add_employee_view, name='addEmployee'),
    path('departments/', views.departments_view, name='departments'),
    path('department/<int:dept_id>/employees/', views.employee_by_department, name='employee_by_department'),
    path('employee/<int:emp_id>/', views.employee_view, name='employee'),
    path('employeeEdit/<int:emp_id>/edit/', views.employee_update, name='edit_employee'),
    path('employee/<int:emp_id>/delete/', views.employee_delete, name='delete_employee'),
  
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
