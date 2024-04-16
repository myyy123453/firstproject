# @Author : Kql
# @Time : 2023/8/25 15:20
# @FileName : urls.py
# @Blog ：https://blog.csdn.net/weixin_56175042
from django.urls import path, re_path
from . import views

app_name = 'file_upload'
urlpatterns = [
    # Upload File Without Using Model Form
    re_path(r'^upload1/$', views.file_upload, name='file_upload'),

    # Upload Files Using Model Form
    # re_path(r'^upload2/$', views.model_form_upload, name='model_form_upload'),

    # View File List
    path('file/', views.file_list, name='file_list'),

]
