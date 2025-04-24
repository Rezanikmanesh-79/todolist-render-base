from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_completed')  
    list_filter = ('is_completed', 'user')  
    search_fields = ('title', 'user__username') 
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # فقط ادمین همه تسک‌ها را می‌بیند
        return queryset.none()  # کاربران عادی چیزی نمی‌بینند

# افزودن لینک گزارش در صفحه اصلی پنل ادمین
def admin_report_link():
    url = reverse('task-report')  # مسیر گزارش در urls.py
    return format_html(f'<a href="{url}" style="font-size:16px; font-weight:bold; color:red;">📊 Task Report</a>')

admin.site.index_title = admin_report_link()  # اضافه کردن لینک به صفحه اصلی ادمین
