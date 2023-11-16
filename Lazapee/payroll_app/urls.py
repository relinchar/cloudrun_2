"""
URL configuration for Lazapee project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.employees, name='employees'),   # @evan: replace the views here with the views for employees page   
    path('payslips', views.payslips, name='payslips'),
    path('addEmployee', views.addEmployee, name='addEmployee'),
    path('updateEmployee/<int:id_number>/', views.updateEmployee, name = 'updateEmployee'),
    path('deleteEmployee/<int:id_number>/', views.deleteEmployee, name = 'deleteEmployee'),
    path('addOvertime/<int:id>/', views.addOvertime, name = 'addOvertime'),
    path('createPayslip', views.createPayslip, name = 'createPayslip'),
    path('viewPayslips/<int:id>/', views.viewPayslips, name='viewPayslips'),
]
