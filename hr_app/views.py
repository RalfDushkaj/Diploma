from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Employee
from .forms import EmployeeForm
from django.contrib import messages


def dashboard_view(request):
    total = Employee.objects.count()
    remote = Employee.objects.filter(work_type='Remote').count()
    onsite = Employee.objects.filter(work_type='Onsite').count()
    on_leave = Employee.objects.filter(work_status='On Leave').count()

    epm_data=[
        {'label': 'Total', 'count': total},
        {'label': 'Remote', 'count': remote},
        {'label': 'Onsite', 'count': onsite},
        {'label': 'On Leave', 'count': on_leave},
    ]

    recent_employees = Employee.objects.order_by('-created_at')[:5]

    dept_data = (
      Employee.objects
      .values('department__name')
      .annotate(count=Count('id'))
  )

    dept_labels = [d['department__name'] for d in dept_data]
    dept_counts = [d['count'] for d in dept_data]

    context = {
        'epm_data': epm_data,
        'recent_employees': recent_employees,
        'remote': remote,
        'onsite': onsite,
        'dept_labels': dept_labels,
        'dept_counts': dept_counts,
    }

    return render(request, 'dashboard.html', context)



def add_employee_view(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully!")
            return redirect('dashboard')
    else:
        form = EmployeeForm()

    return render(request, 'addEmployee.html', {'form': form})

