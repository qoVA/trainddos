"""trainddos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages.views import *
from ddosmodule.views import *

urlpatterns = [
	path('admin/', admin.site.urls),
	path('',home_view, name='home'),
	path('ddosmodule/', include('ddosmodule.urls')),
	path('training/',training, name='training_name'),
	path('strain/<int:id>/',specific_training, name='straining'),
    path('create_content/',content_create_form,name='content_create_form'),
    path('strain/<int:id>/delete/',delete_content,name='delete_content'),
    path('train_list/',train_list,name='train_list_name'),
    path('display_graph/',display_graph,name='display_graph'),
]







	
