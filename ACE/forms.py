# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from AdminConsorcios.models import Factura

class RegistroUsuarios(forms.Form):
	usuario = forms.CharField(label= "Usuario", widget=forms.TextInput())
	email = forms.EmailField(label="Correo Electronico", widget=forms.TextInput())
	clave = forms.CharField(label="Contraseña", widget=forms.PasswordInput(render_value=False))
	clave_conf = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput(render_value=False))
	
class AgregarReclamo(forms.Form):
	fecha = forms.DateField(label="Fecha", widget=forms.DateInput())
	ubicacion = forms.CharField(label="Ubicacion", widget=forms.TextInput())
	descripcion = forms.CharField(label="Descripcion", widget=forms.TextInput())
"""
SERVICIOS = (('Agua'), ('Gas'), ('Luz'), ('Limpieza'), ('Otros'))	
	
class AgregarFacturaConsorcio(forms.Form):
	numero = forms.IntergerField(label= "Numero", widget=forms.NumberInput())
	servicio = forms.MultipleChoiceField(
        required=true,
        widget=forms.CheckboxSelectMultiple,
        choices=SERVICIOS,)
	fechaVencimiento = forms.DateField(widget=forms.SelectDateWidget())
	monto = forms.FloatField(label= "Monto", widget=forms.NumberInput())
	tipo = forms.MultipleChoiceField(
        required=true,
        widget=forms.CheckboxSelectMultiple)
	consorcio = forms.MultipleChoiceField(
        required=true,
        widget=forms.CheckboxSelectMultiple))	
	
	
class FacturaForm(forms.ModelForm):

    class Meta:
        model = Factura
        fields = ['numero', 'servicio', 'gasto', 'abono', 'fechaVencimiento', 'fechaPago', 'monto', 'tipo']

    def __init__(self, *args, **kwargs):
        super(FacturaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
          #  if field <> 'estado':
           #     self.fields[field].widget.attrs.update({
            #        'class': 'form-control'
             #   })	
"""	
class CambiarClave(forms.Form):
	clave_ant = forms.CharField(label="Contraseña Anterior", widget=forms.PasswordInput(render_value=False))
	clave = forms.CharField(label="Nueva Contraseña", widget=forms.PasswordInput(render_value=False))
	clave_conf = forms.CharField(label="Confirmar Nueva Contraseña", widget=forms.PasswordInput(render_value=False))
	
class CambiarEmail(forms.Form):
	email = forms.EmailField(label="Correo Electronico Anterior", widget=forms.TextInput())
	email_nuevo = forms.EmailField(label="Nuevo Correo Electronico ", widget=forms.TextInput())
	
class CambiarUsuario(forms.Form):
	usuario = forms.CharField(label= "Usuario Anterior", widget=forms.TextInput())
	usuario_nuevo = forms.CharField(label= "Nuevo Usuario", widget=forms.TextInput())	

class IniciarSesion(forms.Form):
	usuario = forms.CharField(widget=forms.TextInput())	
	clave = forms.CharField(widget=forms.PasswordInput(render_value=False))

	def validar_usuario(self): # Lo que hace esta funcion es validar para que no existan dos usuarios con el mismo nombre
		usuario = self.cleaned_data["usuario"]
		try:
			usuarios = User.objects.get(username=usuario)
		except User.DoesNotExist:
			return usuario
		raise forms.ValidationError('El nombre de usuario ya existe')
		

	def validar_email(self): #Lo que hace esta funcion es validar para que no existan dos usuarios con el mismo email
		email = self.cleaned_data["email"]
		try:
			emails = User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Ya existe un usuario registrado con ese email')

	def validar_cont_conf(self): #Lo que hace esta funcion es validar las contraseñas para que coincidan
		clave = self.cleaned_data["clave"]
		clave_conf = self.cleaned_data["clave_conf"]
		if clave == clave_conf:
			pass
		else:
			raise forms.ValidationError('Las contraseñas no coinciden')		