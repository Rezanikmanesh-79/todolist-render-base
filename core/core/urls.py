from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name="core/login.html"), name="login"),
    path('logout/', LogoutView.as_view(next_page='/'), name="logout"),
    path('register/', CreateView.as_view(template_name="core/register.html", form_class=UserCreationForm, success_url='/'), name="register"), 
    path('tasks/', include("tasks.urls")),
]
