from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

from .models import Task, Note, SubTask, Category, Priority


def login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')

        if user is not None and not user.is_staff:
            messages.error(request, "This account is not allowed to access the admin panel. Please use a superuser/admin account.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@user_passes_test(lambda user: user.is_authenticated and user.is_staff, login_url='login')
def dashboard_view(request):
    total_tasks = Task.objects.count()
    pending_tasks = Task.objects.filter(status="Pending").count()
    in_progress_tasks = Task.objects.filter(status="In Progress").count()
    completed_tasks = Task.objects.filter(status="Completed").count()

    recent_tasks = Task.objects.select_related('priority', 'category').order_by('-created_at')[:5]

    context = {
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'category_count': Category.objects.count(),
        'priority_count': Priority.objects.count(),
        'note_count': Note.objects.count(),
        'subtask_count': SubTask.objects.count(),
        'recent_tasks': recent_tasks,
    }

    return render(request, 'dashboard.html', context)