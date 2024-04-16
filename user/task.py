# @Author : Kql
# @Time : 2023/7/6 18:18
from django.shortcuts import render

from .models import UserProfile


def dashboard(request):
    user_count = UserProfile.objects.count()
    task_count = UserProfile.objects.count()
    context = {'user_count': user_count, 'task_count': task_count}
    return render(request, 'dashboard.html', context=context)
