from django.contrib import admin
from .models import UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ['username',
                    'nickname',
                    'email',
                    'phone',
                    'info']
    search_fields = ['username', 'nickname']
    list_per_page = 10



admin.site.site_header = 'Kql_Unicorn'  # 设置header
admin.site.site_title = '后台管理'  # 设置title
admin.site.index_title = '博客系统'