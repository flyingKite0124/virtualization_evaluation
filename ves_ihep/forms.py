from django import forms
from ves_ihep.models import Scene, Script, Host

class NewScene(forms.ModelForm):
	class Meta:
		model = Scene
		fields = ('name',)

class DelScene(forms.ModelForm):
	class Meta:
		model = Scene
		fields = ('name',)

"""class NewHost(forms.ModelForm):
	class Meta:
		model = Host
		fields = ('IP','username','passwd',)"""