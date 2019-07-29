from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from ddosmodule.models import *
from ddosmodule.forms import ContentForm, RawContentForm


# Create your views here.

## Home page 
def home_view(request, **kwargs):

	my_context = {
		'title':'HomePage',
	}

	return render(request,'home.html', my_context)

## Registration

def content_create_form(request):
	form = ContentForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = ContentForm()
	context = {
		'form':form
	}

	return render(request,'train/content_create.html', context)

def delete_content(request,id):
	module = get_object_or_404(Content,id=id)

	if request.method =='POST':
		module.delete()
		print('should be deleted')
		return redirect('../')
	
	context={

		'module': module
	}
	
	return render(request, 'train/delete_content.html',context)


def raw_content_create_form(request):

	myform = RawContentForm()

	if request.method =='POST':
		myform = RawContentForm(request.POST)
		if myform.is_valid():
			Content.objects.create(**myform.cleaned_data)
			myform = RawContentForm()
	context = {
		'form':myform
	}

	return render(request,'train/content_create.html', context)