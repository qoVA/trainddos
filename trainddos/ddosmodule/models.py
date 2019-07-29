from django.db import models
from django.urls import reverse

# Create your models here.
class Content(models.Model):
	title = models.CharField( max_length=200, blank=False)
	description = models.TextField(blank=False, null=False)
	study = models.TextField(blank=False, null=False)
	labwork = models.TextField(blank=False, null=False)
	cmd = models.CharField(max_length=200, null=False)
	cmdexp =models.TextField(max_length=200,null=False)
	active = models.BooleanField(default=False)

	def get_absolute_url(self):
		#return f"/strain/{self.id}/"
		return reverse('ddosmodule:straining', kwargs={'id':self.id})