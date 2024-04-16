# @Author : Kql
# @Time : 2023/6/20 14:28
from django.urls import path
from . import views

urlpatterns = [

    path('<str:author_id>', views.TopicViews.as_view())

]
