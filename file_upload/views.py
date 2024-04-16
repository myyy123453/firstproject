from django.shortcuts import render, redirect
from .models import File
from .forms import FileUploadForm,FileUploadModelForm
import os
import uuid
from django.http import JsonResponse
from django.template.defaultfilters import filesizeformat


def file_list(request):
    # 获取所有文件
    files = File.objects.all().order_by("-id")
    # 渲染文件列表页面
    return render(request, "file_upload/file_list.html", {"files": files})


def file_upload(request):
    # 判断请求方法
    if request.method == "POST":
        # 实例化表单
        form = FileUploadForm(request.POST, request.FILES)
        # 判断表单是否有效
        if form.is_valid():
            # get cleaned data
            # 获取表单中的数据
            upload_method = form.cleaned_data.get("upload_method")
            raw_file = form.cleaned_data.get("file")
            # 实例化新文件
            new_file = File()
            # 保存文件
            new_file.file = handle_uploaded_file(raw_file)
            new_file.upload_method = upload_method
            new_file.save()
            # 重定向到文件列表页面
            return redirect("/file/")

    else:
        # 实例化表单
        form = FileUploadForm()
    # 渲染文件上传页面
    return render(request, "file_upload/upload_form.html",
                  {"form": form, 'heading': 'Upload files with Regular Form'})


def handle_uploaded_file(file):
    # 获取文件扩展名
    ext = file.name.split('.')[-1]
    # 创建文件名
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)

    # file path relative to 'media' folder
    # 文件路径
    file_path = os.path.join('files', file_name)
    # 相对路径
    absolute_file_path = os.path.join('media', 'files', file_name)

    # 文件夹
    directory = os.path.dirname(absolute_file_path)
    # 判断文件夹是否存在
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 将文件写入文件夹
    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # 返回文件路径
    return file_path


def model_form_upload(request):
    if request.method == 'POST':
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/file/")
    else:
        form = FileUploadForm()
    return render(request, "file_upload/upload_form.html",
                  {"form": form, 'heading': 'Upload files with Model Form'})
