from django import forms
from .models import Content


class ContentForm(forms.ModelForm):
	class Meta:
		model = Content
		fields = ['title','description','study','labwork','cmd','cmdexp']


class RawContentForm(forms.Form):
	title = forms.CharField( widget = forms.TextInput(attrs = {"placeholder":"Your title"}))
	description = forms.CharField( widget = forms.Textarea)
	study = forms.CharField()
	labwork = forms.CharField()



