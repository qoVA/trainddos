import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from io import BytesIO
import base64
from django.shortcuts import render, get_object_or_404
from .models import Content
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from matplotlib import pylab
from pylab import *
import matplotlib


# Create your views here.
# def training(request):
# object_list = Content.objects.all()
# return render(request,'train/train_list.html',{'modules':object_list})

def training(request):
	
	#object_list = get_object_or_404(Content)
	obj = Content.objects.all()
	paginator = Paginator(obj,1)
	page = request.GET.get('page')

	try:
		modules = paginator.page(page)
	except PageNotAnInteger:
		modules = paginator.page(1)
	except EmptyPage:
	 	modules = paginator.page(paginator.num_pages)


	return render(request,'train/training.html',{ 'modules': modules })



def specific_training(request,id):
	
	obj = get_object_or_404(Content, id=id)
	
	return render(request,'train/training.html',{ 'module':obj })




def train_list(request):

	queryset = Content.objects.all()

	context = {
		'object_list': queryset
	}

	return render(request,'train/train_list.html',context)

def display_graph(request):

    # Construct the graph
	plt.plot([1,2,3,4])
	plt.ylabel('Some numbers')
	buf = BytesIO()
	plt.savefig(buf, format='png', dpi=300)
	image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
	buf.close()

    # Send buffer in a http response the the browser with the mime type image/png set
	return render(request,'train/training.html',{ 'image_base64': image_base64 })

