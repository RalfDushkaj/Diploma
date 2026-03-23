from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Department, Employee, LeaveRequest
from .forms import EmployeeForm
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')




def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
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
        'on_leave': on_leave,
        'dept_labels': dept_labels,
        'dept_counts': dept_counts,
    }

    return render(request, 'dashboard.html', context)




def generate_username(first_name, last_name):
    base = f"{first_name[0]}{last_name[0]}".lower()  
    count = 1
    while True:
        username = f"{base}{count:05d}"  
        if not User.objects.filter(username=username).exists():
            return username
        count += 1




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




def employee_view(request, emp_id):
    employee = Employee.objects.get(id=emp_id)
    return render(request, 'employee.html', {'employee': employee})




def employee_update(request, emp_id):  # <-- use emp_id here
    employee = get_object_or_404(Employee, pk=emp_id)

    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee', emp_id=employee.pk)
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employeeEdit.html', {'form': form, 'employee': employee})




def employee_delete(request, emp_id):
    employee = get_object_or_404(Employee, pk=emp_id)
    employee.delete()
    return redirect('dashboard')




def employee_profile(request):
    # Get the employee object linked to the logged-in user
    employee = Employee.objects.get(user=request.user)

    if request.method == "POST":
        # Handle vacation / leave request
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        reason = request.POST.get("reason")

        # Optional: add validation here (e.g., start < end)
        LeaveRequest.objects.create(
            employee=employee,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status="pending",
        )
        return redirect("employee_profile")  # redirect to avoid double POST

    return render(request, "employee.html", {"employee": employee})



def departments_view(request):
    departments = Department.objects.all()
    return render(request, 'departments.html', {'departments': departments})



def employee_by_department(request, dept_id):
    department = get_object_or_404(Department, pk=dept_id)
    employees = Employee.objects.filter(department=department)
    return render(request, 'employeeList.html', {'department': department, 'employees': employees})
