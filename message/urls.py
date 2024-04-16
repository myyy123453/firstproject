# @Author : Kql
# @Time : 2023/6/27 16:42
from django.urls import path
from . import views

urlpatterns = [
    path('<int:topic_id>', views.message_view)
]
