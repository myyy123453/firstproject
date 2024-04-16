from django.db import models
import os
import uuid


# Create your models here.
def user_directory_path(instance, filename):
    # 文件后缀
    ext = filename.split('.')[-1]
    # 生成全局唯一标志符，并转换为16进制，并取前10位
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join('files', filename)


class File(models.Model):
    file = models.FileField(upload_to=user_directory_path, null=True)
    upload_method = models.CharField(max_length=20, verbose_name="Upload Method")


