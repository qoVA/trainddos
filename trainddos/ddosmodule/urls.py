
from django.urls import path
from pages.views import *
from .views import *

app_name='ddosmodule'

urlpatterns = [
	path('training/',training, name='training_name'),
	path('strain/<int:id>/',specific_training, name='straining'),
    path('create_content/',content_create_form,name='content_create_form'),
    path('strain/<int:id>/delete/',delete_content,name='delete_content'),
    path('train_list/',train_list,name='train_list_name'),
]
