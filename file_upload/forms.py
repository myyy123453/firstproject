# @Author : Kql
# @Time : 2023/8/25 15:23
# @FileName : forms.py
# @Blog ：https://blog.csdn.net/weixin_56175042
# 表单验证

from django import forms
from .models import File


class FileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    upload_method = forms.CharField(label="Upload Method", max_length=20,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_file(self):
        # 获取文件
        file = self.cleaned_data['file']
        # 获取文件后缀
        ext = file.name.split('.')[-1].lower()
        # 判断文件后缀是否为jpg, pdf, xls, xlsx
        if ext not in ['jpg', 'pdf', 'xls', 'xlsx']:
            # 如果不是，抛出错误
            raise forms.ValidationError('Only jpg, pdf and xlsx files are allowed.')
        # 返回文件
        return file


class FileUploadModelForm(forms.ModelForm):
    # 定义表单的元素
    class Meta:
        # 定义表单的模型
        model = File
        # 定义表单的字段
        fields = ['file', 'upload_method']
        # 定义表单的框
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'upload_method': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # 校验文件
    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        # 校验文件类型
        if ext not in ['jpg', 'pdf', 'xls', 'xlsx']:
            raise forms.ValidationError('Only jpg, pdf and xlsx files are allowed.')
        return file
