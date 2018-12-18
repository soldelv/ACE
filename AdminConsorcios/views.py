# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import loader, Context, Template
from django.http import HttpResponse 
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from ACE.forms import RegistroUsuarios, IniciarSesion, AgregarReclamo, CambiarClave 
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from AdminConsorcios.models import *
from django.shortcuts import redirect
from django.utils.dateparse import parse_date
from django.utils.datastructures import MultiValueDictKeyError
import json
import datetime
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger	
from django.shortcuts import render

#----------------------------------------------------------------SESION-----------------------------------------------------------------------------

def inicio(request): # Funcion que me carga el template de la pagina de inicio
	return render_to_response('0 inicio.html', context_instance=RequestContext(request))
		
def registro(request):#Funcion de Registro de Usuarios
	
	if request.method == 'POST':#Si el formulario es enviado
		form = RegistroUsuarios(request.POST)#Creo una instancia del formaulario
		if form.is_valid(): #Si es valido 
			usuario = form.cleaned_data["usuario"]#limpio los datos..
			email = form.cleaned_data["email"]
			clave = form.cleaned_data["clave"]
			clave_conf = form.cleaned_data["clave_conf"]
			usuarios = User.objects.create_user(username=usuario, email=email, password=clave)#Creo el objeto usuario
			usuarios.save() #Guardo el Usuario
			return render_to_response('registrado.html', {'form':form,}, context_instance=RequestContext(request))
	else:#Sino..	
		form = RegistroUsuarios() # Registro vacio
		return render_to_response('registrarse.html', {'form':form,}, context_instance=RequestContext(request))			
			
def iniciarsesion(request):
	mensaje=""
	if request.user.is_authenticated():#Si el usuario esta identificado
	   	return render_to_response('0 inicio.html', context_instance=RequestContext(request)) #redirige al inicio
	else: #sino muestra el login
		if request.method == "POST":#Si el formulario es enviado
			form = IniciarSesion(request.POST)#Creo una instancia del formaulario
			if form.is_valid(): #si es valido
				usuario = form.cleaned_data["usuario"]#limpio los datos..
				clave = form.cleaned_data["clave"]
				persona = authenticate(username=usuario, password=clave)#Lo autentifico
				if persona is not None:#si no es ninguno pregunto
					if persona.is_active:#si esta activo
						login(request,persona)#Lo dejo entrar
						return HttpResponseRedirect('/')#Redirige al inicio de la pagina
				else:
					context = {}
					return render(request, "loginFail.html", context)
		else:
			form = IniciarSesion()
		return render_to_response('login.html', {'form':form}, context_instance=RequestContext(request))


def cerrarsesion(request):#Funcion que me cierra la cesion del usuario
	logout(request)
	return HttpResponseRedirect('/') 	
	
def registroExitoso(request):#Funcion de agradecimiento por registrarte en la pagina
	return render_to_response('registroExitoso.html', context_instance=RequestContext(request))
	
def modificarPerfil(request, id):	#Funcion para mostrar los consorcios en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado
		usuarios = User.objects.get(id=id)
		if request.method == "GET":
			datos={'usuarios':usuarios}
			return render_to_response('modificarPerfil.html', datos, context_instance=RequestContext(request))
		if request.method == "POST":
			resultado = 1
			
			valores = request.POST['valores']
			nombre = request.POST['nombre']
			apellido = request.POST['apellido']
			clave = request.POST['clave']
			clave_conf = request.POST['clave_conf']	
			email = request.POST['email']
			usuario = request.POST['usuario']	
			resultado = 0
			if resultado==0:
				
				if valores=='1':
					usuarios.first_name = nombre
					usuarios.last_name = apellido
					usuarios.save()
					return HttpResponseRedirect('/AdminConsorcios/usuario/perfil/')
				if valores=='2':
					if clave == clave_conf:
						user = request.user
						user.set_password(clave)
						user.save()
						return render_to_response('cambioclave.html', context_instance=RequestContext(request))
					
				if valores=='3':
					usuarios.email = email
					usuarios.save()
					return HttpResponseRedirect('/AdminConsorcios/usuario/perfil/')
				if valores=='4':
					usuarios.username = usuario
					usuarios.save()
					return HttpResponseRedirect('/AdminConsorcios/usuario/perfil/')		
		else:
			context = {}
			return render(request, "modificarPerfil.html", context)
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
		 
def perfil(request):#Funcion de agradecimiento por registrarte en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado
		return render_to_response('perfil.html', context_instance=RequestContext(request))
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')

	
#----------------------------------------------------------------CONSORCIOS-----------------------------------------------------------------------------	

		
def modificarConsorcio(request, id):
	if request.user.is_authenticated():#Si el usuario esta identificado
		consorcios = Consorcio.objects.get(id=id)
		if request.method == "GET":
			datos={'razonsocial':consorcios.razonSocial,'direccion':consorcios.direccion,'localidad':consorcios.localidad,'cp':consorcios.cp,
			'cuit':consorcios.cuit, 'inicioAdministracion':consorcios.inicioAdministracion,	'fechaContratoSocial':consorcios.fechaContratoSocial,
			'actividadEconomica':consorcios.actividadEconomica,	'responsable':consorcios.administrador, 'responsabilidadIVA':consorcios.responsabilidadIVA,
			'suterh':consorcios.suterh, 'clave':consorcios.clavesuterh, 'cc':consorcios.cantidadCocheras, 'unidadfuncional':consorcios.cantidadUnidadesFuncionales,
			'cantidadAsensores':consorcios.cantidadAsensores,'cantidadCalderas':consorcios.cantidadCalderas, 'instalaciones':consorcios.instalacionesFijas, 'agencia':consorcios.agencia,
			'categoria':consorcios.categoria, 'termotanque':consorcios.cantidadTermotanques}
			return render_to_response('modificarConsorcios.html', datos, context_instance=RequestContext(request))
		if request.method == "POST":
			res = 1
			razonsocial = request.POST['razonsocial']
			direccion = request.POST['direccion']
			cp = request.POST['cp']
			localidad = request.POST['localidad']
			cuit = request.POST['cuit']
			cc = request.POST['cc']
			unidadfuncional = request.POST['unidadfuncional']
			actividadEconomica = request.POST['actividadEconomica']
			responsable = request.POST['responsable']
			suterh = request.POST['suterh']
			responsabilidadIVA = request.POST['responsabilidadIVA']
			inicioAdministracion = request.POST['inicioAdministracion']
			fechaContratoSocial = request.POST['fechaContratoSocial']
			cantidadAsensores = request.POST['cantidadAsensores']
			cantidadCalderas = request.POST['cantidadCalderas']	
			instalaciones = request.POST['instalaciones']	
			clave = request.POST['clave']	
			agencia = request.POST['agencia']	
			categoria = request.POST['categoria']	
			termotanque = request.POST['termotanque']
			res = 0
			if res==0 :
				consorcios = Consorcio.objects.get(id=id)
				consorcios.razonSocial = razonsocial				
				consorcios.direccion = direccion
				consorcios.localidad = localidad
				consorcios.cp = cp
				consorcios.cuit = cuit
				consorcios.inicioAdministracion = inicioAdministracion
				consorcios.fechaContratoSocial = fechaContratoSocial
				consorcios.actividadEconomica = actividadEconomica
				consorcios.administrador = responsable
				consorcios.responsabilidadIVA = responsabilidadIVA
				consorcios.suterh = suterh
				consorcios.clavesuterh = clave
				consorcios.cantidadCocheras = cc
				consorcios.cantidadUnidadesFuncionales = unidadfuncional
				consorcios.cantidadAsensores = cantidadAsensores
				consorcios.cantidadCalderas = cantidadCalderas
				consorcios.instalacionesFijas = instalaciones
				consorcios.agencia = agencia
				consorcios.categoria = categoria
				consorcios.cantidadTermotanques = termotanque
				consorcios.save()
				context = {}
				return render(request, "accionExitosa.html", context)
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')			
			
def agregarConsorcio(request):	#Funcion para agregar los consorcios en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			numero=2
			razonsocial = request.POST['razonsocial']
			direccion = request.POST['direccion']
			cp = request.POST['cp']
			localidad = request.POST['localidad']
			cuit = request.POST['cuit']
			cc = request.POST['cc']
			unidadfuncional = request.POST['unidadfuncional']
			actividadEconomica = request.POST['actividadEconomica']
			responsable = request.POST['responsable']
			suterh = request.POST['suterh']
			responsabilidadIVA = request.POST['responsabilidadIVA']
			inicioAdministracion = request.POST['inicioAdministracion']
			fechaContratoSocial = request.POST['fechaContratoSocial']
			cantidadAsensores = request.POST['cantidadAsensores']
			cantidadCalderas = request.POST['cantidadCalderas']	
			instalaciones = request.POST['instalaciones']	
			clave = request.POST['clave']	
			agencia = request.POST['agencia']	
			categoria = request.POST['categoria']	
			termotanque = request.POST['termotanque']	
			resultado = 0
			if resultado==0:
				admin = Administracion.objects.get( id = 1 )#El ID es 1 porque solo hay una administracion
				consorcios = Consorcio.objects.filter(razonSocial=razonsocial) #Verifico si el consorcio existe, False no y lo agrego
				if consorcios.exists() == False:
					admin = Administracion.objects.get(id=1)#El ID es 1 porque solo hay una administracion
					consorcios = Consorcio.objects.create(administracion_id = admin.id,razonSocial=razonsocial, direccion=direccion, cp=cp, localidad=localidad, cuit=cuit, 
					cantidadCocheras=cc, cantidadUnidadesFuncionales=unidadfuncional, actividadEconomica=actividadEconomica, administrador=responsable,
					suterh=suterh, responsabilidadIVA=responsabilidadIVA, numero=numero, inicioAdministracion=inicioAdministracion, fechaContratoSocial=fechaContratoSocial,
					cantidadAsensores=cantidadAsensores, cantidadCalderas=cantidadCalderas, instalacionesFijas=instalaciones, clavesuterh=clave, cantidadTermotanques=termotanque,
					agencia=agencia, categoria=categoria)	
					consorcios.save()
					context = {}
					return render(request, "accionExitosa.html", context)
				else:
					context = {}
					return render(request, "agregarConsorcio.html", context)
		
		else:
			context = {}
			return render(request, "agregarConsorcio.html", context)
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')

def mostrarConsorcio(request):  # Funcion para mostrar los consorcios en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			valor = request.POST['valor']
			consorcio = request.POST['consorcio']
			resultado = 0
			if resultado == 0:
				if valor == '2':
					consorcios1 = Consorcio.objects.all().filter(esBaja = 0)
					return render_to_response('consorcios.html', {'consorcios1': consorcios1}, context_instance=RequestContext(request))
				if valor == '1':
					consorcios = Consorcio.objects.filter(id=consorcio)  # Traigo los consorcios por nombre y los que no fueron dados de baja
					if consorcios.exists() == True:
						return render_to_response('consorcio.html', {'consorcios': consorcios}, context_instance=RequestContext(request))
					else:
						context = {}
						return render(request, "mostrarConsorcios2.html", context)
		else:
			consorcios = Consorcio.objects.all()
			return render_to_response('mostrarConsorcios.html', {'consorcios': consorcios}, context_instance=RequestContext(request))
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')  
									  
def busquedaConsorcio(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			consorcio = request.POST['consorcio']
			resultado = 0
			if resultado==0:
					consorcios = Consorcio.objects.filter(id=consorcio)#Traigo los consorcios por nombre
					return render_to_response('consorcio.html', {'consorcios':consorcios}, context_instance=RequestContext(request))
		else:
			return render_to_response('busqueda.html', context_instance=RequestContext(request))
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/') 	
		
def mostrarConsorcioArchivado(request):	#Funcion para mostrar los consorcios en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			valor = request.POST['valor']
			consorcio = request.POST['consorcio']
			resultado = 0
			if resultado==0:
				if valor=='2':
					con = Consorcio.objects.all().filter(esBaja = 1)#Traigo todos los consorcios archivados
					return render_to_response('consorcios.html', {'consorcios1':con}, context_instance=RequestContext(request))
				if valor=='1':
					consorcios = Consorcio.objects.filter(id=consorcio, esBaja=1)#Traigo los consorcios por nombre y los que fueron dados de baja
					return render_to_response('consorcio.html', {'consorcios':consorcios}, context_instance=RequestContext(request))
		else:
			return render_to_response('mostrarConsorcioArchivado.html', context_instance=RequestContext(request))
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')	
	
def archivarConsorcio(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			consorcio = request.POST['consorcio']
			valor = request.POST['valor']
			resultado = 0
			if resultado == 0:
				consorcios = Consorcio.objects.filter(id=consorcio)  # Verifico si el consorcio existe, False no y lo agrego
				if consorcios.exists() == True:
					con = Consorcio.objects.get(id=consorcio)
					if valor == '1':
						con.esBaja = 1  # El consorcio es dado de baja (esBaja=true)
						con.save()
						context = {}
						return render(request, "accionExitosa.html", context)	
					elif valor == '2':
						context = {}
						return render(request, "accionExitosa.html", context)	
				else:
					context = {}
					return render(request, "archivarConsorcio2.html", context)
		else:
			context = {}
			return render(request, "archivarConsorcio.html", context)
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')	
					
#----------------------------------------------------------------UNIDADES FUNCIONALES-----------------------------------------------------------------------------

def agregarUnidadFuncional(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			consorcio = request.POST['consorcio']
			estaAlquilado = request.POST['estaAlquilado']
			depto = request.POST['depto']
			piso = request.POST['piso']  # ES LA UNIDAD FUNCIONAL!!!!!!!!!!!!!
			valores = request.POST['valores']

			# Propietario
			nombre = request.POST['nombre']
			apellido = request.POST['apellido']
			dni = request.POST['dni']
			email = request.POST['email']
			telFijo = request.POST['telFijo']
			celular = request.POST['celular']
			localidad = request.POST['localidad']
			cp = request.POST['cp']
			direccion = request.POST['direccion']

			# Inquilino
			nombres = request.POST['nombres']
			apellidos = request.POST['apellidos']
			dnis = request.POST['dnis']
			emails = request.POST['emails']
			telFijos = request.POST['telFijos']
			celulars = request.POST['celulars']
			resultado = 0
			if resultado == 0:
				consorcios = Consorcio.objects.filter(id=consorcio)  # Verifico si el consorcio existe,
				UF = UnidadFuncional.objects.filter(consorcio_id=consorcio, unidadFuncional=piso);
				if consorcios.exists() == True:
					if UF.exists() == False:  # TENGO QUE VERIFICAR QUE NO EXISTA LA Unidad FUNCIONAL
						if valores == '0':  # SI  esta creado el propietario

							propietarioValidado = Propietario.objects.filter(dni=dni)
							if propietarioValidado.exists() == True:
								context = {}
								return render(request, "ingresarUnidadFuncionalFuncionSi.html", context)	
							
								# prop = Propietario.objects.get(
									# dni=dni)  # Traigo el propietario por dni para poder asociarlo a la unidad funcional
								# cons = Consorcio.objects.get(
									# id=consorcio)  # Trago el consorcio por razon social para poder asociarlo a la unidad funcional
								# if estaAlquilado == '0':
									#prop.direccion = direccion#le agrego la direccion
									#prop.save()
									# inquilinos = Inquilino.objects.create(nombre=nombres, apellido=apellidos, dni=dnis,
																		  # email=emails, telFijo=telFijos, celular=celulars)
									# inquilinos.save()
									# inq = Inquilino.objects.get(
										# dni=dnis)  # Traigo el inquilino por dni para poder asociarlo a la unidad funcional
									# unidad = UnidadFuncional.objects.create(consorcio_id=cons.id, propietario_id=prop.id,
																			# inquilino_id=inq.id, alquilado=1,
																			# unidadFuncional=piso, pisoDepartamento=depto)
									# unidad.save()
									

							  #  else:
									# unidades = UnidadFuncional.objects.create(consorcio_id=cons.id, propietario_id=prop.id,
																			  # alquilado=0, unidadFuncional=piso,
																			  # pisoDepartamento=depto)
									# unidades.save()
									# return HttpResponseRedirect('/')
							else:
								context = {}
								return render(request, "ingresarUnidadFuncional.html", context)
						elif valores == '1':  # si no esta creado

							# pro = Propietario.objects.get(dni=dni) #Traigo el propietario por dni para poder asociarlo a la unidad funcional
							con = Consorcio.objects.get(id=consorcio)  # Trago el consorcio por razon social para poder asociarlo a la unidad funcional
							if estaAlquilado == '0':
								propietarios = Propietario.objects.create(nombre=nombre, apellido=apellido, dni=dni,
																		  email=email, direccion=direccion, telFijo=telFijo,
																		  celular=celular, cp=cp, localidad=localidad)
								
								inquilinos = Inquilino.objects.create(nombre=nombres, apellido=apellidos, dni=dnis,
																	  email=emails, telFijo=telFijos, celular=celulars)
								propietarios.save()
								inquilinos.save()
								unidad = UnidadFuncional.objects.create(consorcio_id= con.id, propietario_id=propietarios.id ,inquilino_id=inquilinos.id, alquilado=1,unidadFuncional=piso, pisoDepartamento=depto)
								unidad.save()

								context = {}
								return render(request, "accionExitosa.html", context)	
							else:
								pro = Propietario.objects.create(nombre=nombre, apellido=apellido, dni=dni, email=email,
																 telFijo=telFijo, celular=celular, cp=cp,
																 localidad=localidad)
								pro.save()
								unidades = UnidadFuncional.objects.create(consorcio_id=con.id, propietario_id=pro.id,
																		  alquilado=0, unidadFuncional=piso,
																		  pisoDepartamento=depto)
								unidades.save()
								context = {}
								return render(request, "accionExitosa.html", context)	
					else:
						context = {}
						return render(request, "ingresarUnidadFuncional.html", context)
				else:
					context = {}
					return render(request, "ingresarUnidadFuncional2.html", context)
		else:
			context = {}
			return render(request, "ingresarUnidadFuncional.html", context)
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')		
	
		
def modificarUnidadFuncional(request, id):
	if request.user.is_authenticated():#Si el usuario esta identificado
		unidadFuncional = UnidadFuncional.objects.get(id = id)
		if request.method == "GET":
			datos={'consorcio':unidadFuncional.consorcio,'propietario':unidadFuncional.propietario,'inquilino':unidadFuncional.inquilino,'alquilado':unidadFuncional.alquilado,
			'unidadFuncional':unidadFuncional.unidadFuncional, 'pisoDepartamento':unidadFuncional.pisoDepartamento}
			return render_to_response('modificarUnidadFuncional.html', datos, context_instance=RequestContext(request))

		if request.method == "POST":
			resultado = 1
			consorcio = request.POST['consorcio']
			estaAlquilado = request.POST['estaAlquilado']
			depto = request.POST['depto'] #Piso y Departamento
			dato = request.POST['dato']  #¿Desea Modificar los Datos del Propietario?
			
			#Propietario
			nombre = request.POST['nombre']
			apellido = request.POST['apellido']
			dni = request.POST['dni']
			email = request.POST['email']
			telFijo = request.POST['telFijo']
			celular = request.POST['celular']
			localidad = request.POST['localidad']
			direccion = request.POST['direccion']
			cp = request.POST['cp']
			
			#Inquilino
			nombres = request.POST['nombres']
			apellidos = request.POST['apellidos']
			dnis = request.POST['dnis']
			emails = request.POST['emails']
			telFijos = request.POST['telFijos']
			celulars = request.POST['celulars']
			resultado = 0
			if resultado==0:
				validacionConsorcio = Consorcio.objects.filter(id = consorcio) #Verifico si el consorcio existe para modificarlo
				if validacionConsorcio.exists() == True: #CONSORCIO EXISTENTE
					con = Consorcio.objects.get(id=consorcio)
					unidadFuncional.consorcio.id = consorcio
					unidadFuncional.pisoDepartamento = depto
					if dato == '0': #Quiero modificar los datos del propietario
						propietario = Propietario.objects.get(id = unidadFuncional.propietario_id)
						propietario.nombre=nombre
						propietario.apellido=apellido
						propietario.dni=dni
						propietario.email=email
						propietario.telFijo=telFijo
						propietario.celular=celular
						propietario.direccion = direccion
						propietario.cp=cp
						propietario.localidad=localidad
						propietario.save()
						context = {}
						return render(request, "accionExitosa.html", context)	
						if estaAlquilado == True: #Si quiero alquilarlo
							if unidadFuncional.alquilado == '1': #Si modifico a alquilado y ya estaba alquilado, solo modifico datos
								inquilino = Inquilino.objects.get(id = unidadFuncional.inquilino)
								inquilino.nombre = nombres
								inquilino.apellido = apellidos
								inquilino.dni = dnis
								inquilino.email = emails
								inquilino.telFijo = telFijos
								inquilino.celular = celulars
								inquilino.save()
								unidadFuncional.save()
								context = {}
								return render(request, "accionExitosa.html", context)	
							else:# Si modifico a alquilado y no estaba alquilado, lo creo
								inquilinos = Inquilino.objects.create(nombre=nombres, apellido=apellidos, dni=dnis,
																	  email=emails, telFijo=telFijos, celular=celulars)
								inquilinos.save()
								unidadFuncional.inquilino_id = Inquilino.objects.get(dni = dnis).id
								unidadFuncional.save()
								context = {}
								return render(request, "accionExitosa.html", context)	
						else: #Si pongo que no sera alquilado y ya estaba alquilado
							if unidadFuncional.alquilado == '1':
								inquilino = Inquilino.objects.get(id = unidadFuncional.inquilino)
								unidadFuncional.inquilino = 0 # LE PONGO 0 porque no se puede eliminar como NONE
								unidadFuncional.alquilado = '0'
								unidadFuncional.save()#	
								inquilino.delete()
								context = {}
								return render(request, "accionExitosa.html", context)	
					else: #NO QUIERO MODIFICAR LOS DATOS DEL PROPIETARIO
						if estaAlquilado == True: #Si quiero alquilarlo
							if unidadFuncional.alquilado == '1': #Si modifico a alquilado y ya estaba alquilado, solo modifico datos
								inquilino = Inquilino.objects.get(id = unidadFuncional.inquilino)
								inquilino.nombre = nombres
								inquilino.apellido = apellidos
								inquilino.dni = dnis
								inquilino.email = emails
								inquilino.telFijo = telFijos
								inquilino.celular = celulars
								inquilino.save()
								unidadFuncional.save()#	
								context = {}
								return render(request, "accionExitosa.html", context)	
							else:# Si modifico a alquilado y no estaba alquilado, lo creo
								inquilino = Inquilino.objects.create(nombre=nombres, apellido=apellidos, dni=dnis, email=emails, telFijo=telFijos, celular=celulars)
								inquilino.save()
								unidadFuncional.inquilino_id = inquilino.id
								unidadFuncional.save()
								context = {}
								return render(request, "accionExitosa.html", context)	
						else: #Si pongo que no sera alquilado y ya estaba alquilado
							if unidadFuncional.alquilado == '1':
								unidadFuncional
								inquilino = Inquilino.objects.get(id = unidadFuncional.inquilino)
								unidadFuncional.inquilino = 0 # LE PONGO 0 porque no se puede eliminar como NONE
								unidadFuncional.alquilado = '0'
								unidadFuncional.save()#	
								inquilino.delete()
								unidadFuncional.save()
								context = {}
								return render(request, "accionExitosa.html", context)	
							else:
								unidadFuncional.alquilado = '0'
								unidadFuncional.save()
								context = {}
								return render(request, "accionExitosa.html", context)	
				else:
					context = {}
					return render(request, "agregarConsorcio.html", context)
		else:
			context = {}
			return render(request, "modificarUnidadFuncional.html", context)	
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')	

def mostrarUnidadFuncional(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1	
			consorcio = request.POST['consorcio']
			resultado = 0
			if resultado==0:
				consorcios = Consorcio.objects.filter(id=consorcio) #Verifico si el consorcio existe, 
				if consorcios.exists() == True:
					con = Consorcio.objects.get(id=consorcio)
					unidades = UnidadFuncional.objects.all().filter(consorcio_id=con.id)
					return render_to_response('unidadesFuncionales.html', {'unidades':unidades}, context_instance=RequestContext(request))	
				else:
					context = {}
					return render(request, "agregarConsorcio.html", context)		
		else:
			context = {}
			return render(request, "mostrarUnidadFuncional.html", context)		
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
#----------------------------------------------------------------EMPLEADOS-----------------------------------------------------------------------------


def eliminarEmpleado(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			valor = request.POST['valor']
			dni = request.POST['dni']
			resultado = 0
			if resultado==0:
				verificacionEmpleado = Empleado.objects.filter(dni = dni)
				if verificacionEmpleado.exists() == True: #VERIFICO QUE EL EMPLEADO EXISTA
					empleado = Empleado.objects.get(dni=dni)
					if valor=='1':
						empleado.delete()
						context = {}
						return render(request, "accionExitosa.html", context)	
					elif valor=='2':
						context = {}
						return render(request, "eliminarEmpleado.html", context)
				else:
					context = {}
					return render(request, "eliminarEmpleadoError.html", context)
		else:
			context = {}
			return render(request, "eliminarEmpleado.html", context)
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')		

def modificarEmpleado(request, id):
	if request.user.is_authenticated():#Si el usuario esta identificado
		empleado = Empleado.objects.get(id=id)

		if request.method == "GET":
			datos = {'empleado': empleado}
			return render_to_response('modificarEmpleados.html', datos, context_instance=RequestContext(request))

		if request.method == "POST":
			resultado = 1
			dato = request.POST['dato']  # CAMBIA DATOS
			dni = request.POST['dni']
			nombre = request.POST['nombre']
			apellido = request.POST['apellido']
			cuil = request.POST['cuil']
			email = request.POST['email']
			nacionalidad = request.POST['nacionalidad']
			telFijo = request.POST['telFijo']
			celular = request.POST['celular']
			direccion = request.POST['direccion']
			localidad = request.POST['localidad']
			cp = request.POST['cp']
			fechaNacimiento = request.POST['fechaNacimiento']
			fechaIngreso = request.POST['fechaIngreso']
			funcion = request.POST['funcion']
			categoria = request.POST['categoria']
			estadocivil = request.POST['estadocivil']
			estudios = request.POST['estudios']
			observaciones = request.POST['observaciones']
			if dato == '1':
				#			valor = request.POST['valor']
				# consorcio = request.POST['consorcio']
				trabajaSemana = request.POST['trabajaSemana']
				trabajaFinde = request.POST['trabajaFinde']
				horarioFeriado = request.POST['horarioFeriado']

				if trabajaSemana == '0':  # si trabaja en la semana
					horarioInicio = request.POST['horarioInicio']
					horarioFin = request.POST['horarioFin']
					horarioAdicional = request.POST['horarioAdicional']
					if horarioAdicional == '0':  # si trabaja en mas de un turno
						horarioAdicionalSemanalInicio = request.POST['horarioAdicionalSemanalInicio']
						horarioAdicionalSemanalFin = request.POST['horarioAdicionalSemanalFin']
				if trabajaFinde == '0':  # trabaja el sabado
					horarioSabadoInicio = request.POST['horarioSabadoInicio']
					horarioSabadoFin = request.POST['horarioSabadoFin']
					horarioAdicionalSabado = request.POST['horarioAdicionalSabado']
					if horarioAdicionalSabado == '0':  # si trabaja en mas de un turno
						horarioAdicionalSabadoInicio = request.POST['horarioAdicionalSabadoInicio']
						horarioAdicionalSabadoFin = request.POST['horarioAdicionalSabadoFin']
				if trabajaFinde == '1':  # si trabaja el domingo
					horarioDomingoInicio = request.POST['horarioDomingoInicio']
					horarioDomingoFin = request.POST['horarioDomingoFin']
					horarioAdicionalDomingo = request.POST['horarioAdicionalDomingo']
					if horarioAdicionalDomingo == '0':  # si trabaja en mas de un turno
						horarioAdicionalDomingoInicio = request.POST['horarioAdicionalDomingoInicio']
						horarioAdicionalDomingoFin = request.POST['horarioAdicionalDomingoFin']
				if trabajaFinde == '2':  # si trabaja sabado y domingo
					horarioSabadoInicio = request.POST['horarioSabadoInicio']
					horarioSabadoFin = request.POST['horarioSabadoFin']
					horarioAdicionalSabado = request.POST['horarioAdicionalSabado']
					if horarioAdicionalSabado == '0':  # si trabaja en mas de un turno
						horarioAdicionalSabadoInicio = request.POST['horarioAdicionalSabadoInicio']
						horarioAdicionalSabadoFin = request.POST['horarioAdicionalSabadoFin']
					horarioDomingoInicio = request.POST['horarioDomingoInicio']
					horarioDomingoFin = request.POST['horarioDomingoFin']
					horarioAdicionalDomingo = request.POST['horarioAdicionalDomingo']
					if horarioAdicionalDomingo == '0':  # si trabaja en mas de un turno
						horarioAdicionalDomingoInicio = request.POST['horarioAdicionalDomingoInicio']
						horarioAdicionalDomingoFin = request.POST['horarioAdicionalDomingoFin']
					if horarioFeriado == '0':  # si trabaja los feriados
						horarioFeriadoInicio = request.POST['horarioFeriadoInicio']
						horarioFeriadoFin = request.POST['horarioFeriadoFin']
						horarioAdicionalFeriado = request.POST['horarioAdicionalFeriado']
						if horarioAdicionalFeriado == '0':  # si trabaja en mas de un turno
							horarioAdicionalFeriadoInicio = request.POST['horarioAdicionalFeriadoInicio']
							horarioAdicionalFeriadoFin = request.POST['horarioAdicionalFeriadoFin']
			resultado = 0
			if resultado == 0:
				if dato == '2':
					empleado.dni = dni
					empleado.nombre = nombre
					empleado.apellido = apellido
					empleado.cuil = cuil
					empleado.email = email
					empleado.nacionalidad = nacionalidad
					empleado.telFijo = telFijo
					empleado.celular = celular
					empleado.direccion = direccion
					empleado.localidad = localidad
					empleado.cp = cp
					empleado.fechaNacimiento = fechaNacimiento
					empleado.ingreso = fechaIngreso
					empleado.funcion = funcion
					empleado.categoriaFuncion = categoria
					empleado.estadoCivil = estadocivil
					empleado.estudios = estudios
					empleado.observaciones = observaciones
					empleado.save()
					return HttpResponseRedirect('/')

				else:
					empleado.dni = dni
					empleado.nombre = nombre
					empleado.apellido = apellido
					empleado.cuil = cuil
					empleado.email = email
					empleado.nacionalidad = nacionalidad
					empleado.telFijo = telFijo
					empleado.celular = celular
					empleado.direccion = direccion
					empleado.localidad = localidad
					empleado.cp = cp
					empleado.fechaNacimiento = fechaNacimiento
					empleado.ingreso = fechaIngreso
					empleado.funcion = funcion
					empleado.categoriaFuncion = categoria
					empleado.estadoCivil = estadocivil
					empleado.estudios = estudios
					empleado.observaciones = observaciones

					if trabajaSemana == '0' and horarioFeriado == '1':  # si trabaja en la semana, pero no trabaja feriados
						if horarioAdicional == '0':  # si tiene horario adicional
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1':  # si no tiene horario adicional

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.save()
							return HttpResponseRedirect('/')

					elif trabajaSemana == '0' and horarioFeriado == '0':  # si trabaja en la semana y trabaja feriados
						if horarioAdicional == '0' and horarioAdicionalFeriado == '1':  # si tiene horario adicional, pero no los feriados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalFeriado == '0':  # si tiene horario adicional en la semana y tambien en los feriados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalFeriado == '1':  # si no tiene horario adicional en la semana y en los feriados

							empleado.horarioSemanalInicio = horarioInicio,
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio,
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalFeriado == '0':  # si no tiene horario adicional en la semana, pero si en los feriados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

					elif trabajaSemana == '0' and trabajaFinde == '0' and horarioFeriado == '1':  # si trabaja en la semana y trabaja los sabados
						if horarioAdicional == '0' and horarioAdicionalSabado == '1':  # si tiene horario adicional, pero no los sabados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio,
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalSabado == '0':  # si tiene horario adicional en la semana y tambien los sabados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '1':  # si no tiene horario adicional en la semana y los sabados
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '0':  # si no tiene horario adicional en la semana, pero si los sabados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.save()
							return HttpResponseRedirect('/')

					# Trabaja Feriados ademas de los dias en los que trabaja
					elif trabajaSemana == '0' and trabajaFinde == '0' and horarioFeriado == '0':  # si trabaja en la semana y trabaja los sabados
						if horarioAdicional == '0' and horarioAdicionalSabado == '1' and horarioAdicionalFeriado == '1':  # si tiene horario adicional solo en la semana, pero no los sabados y feriados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalSabado == '0' and horarioAdicionalFeriado == '1':  # si tiene horario adicional en la semana y tambien los sabados, pero no los feriados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '1' and horarioAdicionalFeriado == '1':  # si no tiene horario adicional en la semana y los sabados y feriados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.fechaNacimiento = fechaNacimiento
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '0' and horarioAdicionalFeriado == '1':  # si no tiene horario adicional en la semana y en los feriados, pero si los sabados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalSabado == '1' and horarioAdicionalFeriado == '0':  # si tiene horario adicional en la semana y en los feriados, pero no los sabados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin,
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalSabado == '0' and horarioAdicionalFeriado == '0':  # si tiene horario adicional en la semana, los sabados y tambien en los feriados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '1' and horarioAdicionalFeriado == '0':  # si no tiene horario adicional en la semana y los sabados, pero si los feriados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '0' and horarioAdicionalFeriado == '0':  # si no tiene horario adicional en la semana, pero si los sabados y feriados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

					elif trabajaSemana == '0' and trabajaFinde == '1' and horarioFeriado == '1':  # si trabaja en la semana y trabaja los domingos
						if horarioAdicional == '0' and horarioAdicionalDomingo == '1':  # si tiene horario adicional, pero no los sabados

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin,
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalDomingo == '0':  # si tiene horario adicional en la semana y tambien los domingos

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioDomingoInicio = horarioDomingoInicio, horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalDomingo == '1':  # si no tiene horario adicional en la semana y los domingos

							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalDomingo == '0':  # si no tiene horario adicional en la semana, pero si los domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')

					# Ademas de los dias en los que trabaja tambien lo hace los feriados
					elif trabajaSemana == '0' and trabajaFinde == '1' and horarioFeriado == '0':  # si trabaja en la semana y trabaja los domingos
						if horarioAdicional == '0' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '1':  # si tiene horario adicional en la semana, pero no los sabados y feriados
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '1':  # si tiene horario adicional en la semana y tambien los domingos, pero no los feriados
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '1':  # si no tiene horario adicional en la semana, los domingos y feriados
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '1':  # si no tiene horario adicional en la semana y los feriados, pero si los domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '0':  # si tiene horario adicional en la semana y los feriados, pero no los domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '0':  # si tiene horario adicional en la semana y tambien los domingos y feriados
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '0':  # si no tiene horario adicional en la semana y los domingos, pero si los feriados
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin,
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio,
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '0':  # si no tiene horario adicional en la semana, pero si los domingos y feriados
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

					elif trabajaSemana == '0' and trabajaFinde == '2' and horarioFeriado == '1':  # si trabaja en la semana y trabaja los sabados y domingos, pero no los feriados
						if horarioAdicional == '0' and horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '1':  # si tiene horario adicional en la semana, pero no los sabados y domingos
							empleado.empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '0':  # si tiene horario adicional en la semana y tambien los sabados y domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional == '1' and horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '0':  # si no tiene horario adicional en la semana y los sabados, pero si los domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin,
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional == '1' and horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '0':  # si no tiene horario adicional en la semana, pero si los sabados y domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional == '1' and horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '1':  # si no tiene horario adicional en la semana y domingos, pero si los sabados
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional == '0' and horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '0':  # si tiene horario adicional en la semana y los domingos, pero no los sabados
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '1':  # si no tiene horario adicional en la semana y tambien los sabados y domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '1':  # si tiene horario adicional en la semana y sabados, pero no los domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.save()
							return HttpResponseRedirect('/')

					elif trabajaSemana == '0' and trabajaFinde == '2' and horarioFeriado == '0':  # si trabaja en la semana y trabaja los sabados y domingos y los feriados
						# No Trabaja adicional los feriados--------------------------------------------------------------------------------------------
						if horarioAdicional == '0' and horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '1':  # si tiene horario adicional en la semana, pero no los sabados y domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSabadoFin = horarioSabadoFin, horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '1':  # si tiene horario adicional en la semana y tambien los sabados y domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '1':  # si no tiene horario adicional en la semana y los sabados, pero si los domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '1':  # si no tiene horario adicional en la semana, pero si los sabados y domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '1':  # si no tiene horario adicional en la semana y domingos, pero si los sabados
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '1':  # si tiene horario adicional en la semana y los domingos, pero no los sabados
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '1':  # si no tiene horario adicional en la semana y tambien los sabados y domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '1':  # si tiene horario adicional en la semana y sabados, pero no los domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						# Trabaja adicional los feriados--------------------------------------------------------------------------------------------
						elif horarioAdicional == '0' and horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '0':  # si tiene horario adicional en la semana, pero no los sabados y domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '0':  # si tiene horario adicional en la semana y tambien los sabados y domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '0':  # si no tiene horario adicional en la semana y los sabados, pero si los domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '0':  # si no tiene horario adicional en la semana, pero si los sabados y domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '0':  # si no tiene horario adicional en la semana y domingos, pero si los sabados
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '0':  # si tiene horario adicional en la semana y los domingos, pero no los sabados
							empleado.horarioSemanalInicio = horarioInicio, horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
							empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '1' and horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '0':  # si no tiene horario adicional en la semana y tambien los sabados y domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

						elif horarioAdicional == '0' and horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '0':  # si tiene horario adicional en la semana y sabados, pero no los domingos
							empleado.horarioSemanalInicio = horarioInicio
							empleado.horarioSemanalFin = horarioFin
							empleado.horarioFeriadoFin = horarioFeriadoFin
							empleado.horarioSemanalAdicionalInicio = horarioAdicionalSemanalInicio
							empleado.horarioSemanalAdicionalFin = horarioAdicionalSemanalFin
							empleado.horarioFeriadoInicio = horarioFeriadoInicio
							empleado.horarioSabadoFin = horarioSabadoFin
							empleado.horarioSabadoInicio = horarioSabadoInicio
							empleado.horarioDomingoInicio = horarioDomingoInicio
							empleado.horarioDomingoFin = horarioDomingoFin
							empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
							empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
							empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
							empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
							empleado.save()
							return HttpResponseRedirect('/')

					elif trabajaSemana == '1' and horarioFeriado == '1':  # si no trabaja en la semana y no tampoco los feriados
						if trabajaFinde == '0':  # trabaja el sabado
							if horarioAdicionalSabado == '0':  # si trabaja en mas de un turno
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
								empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
								empleado.save()
								return HttpResponseRedirect('/')

							else:
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.save()
								return HttpResponseRedirect('/')
						elif trabajaFinde == '1':  # trabaja el domingo
							if horarioAdicionalDomingo == '0':  # si trabaja en mas de un turno
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
								empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
								empleado.save()
								return HttpResponseRedirect('/')
							else:
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.save()
								return HttpResponseRedirect('/')
						elif trabajaFinde == '2':  # trabaja el sabado y el domingo
							if horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '1':  # si trabaja en mas de un turno el sabado
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
								empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '1':
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalDomingo == '0' and horarioAdicionalSabado == '1':  # si trabaja en mas de un turno el domingo
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
								empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalDomingo == '0' and horarioAdicionalSabado == '0':
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
								empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
								empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
								empleado.save()
								return HttpResponseRedirect('/')
					# elif trabajaFinde=='3':#si no trabaja sabado y domingo
					# return HttpResponseRedirect('/')
					elif trabajaSemana == '1' and horarioFeriado == '0':  # si no trabaja en la semana, pero si los feriados
						if trabajaFinde == '0' and horarioFeriado == '1':  # trabaja el sabado, pero no los feriados
							if horarioAdicionalSabado == '0':  # si trabaja en mas de un turno
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
								empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							else:
								empleado.horarioSabadoInicio = horarioSabadoInicio,
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.save()
								return HttpResponseRedirect('/')
						elif trabajaFinde == '0' and horarioFeriado == '0':  # trabaja el sabado y los feriados
							if horarioAdicionalSabado == '0' and horarioAdicionalFeriado == '1':  # si trabaja en mas de un turno los sabados, pero no los feriados
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
								empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado == '0' and horarioAdicionalFeriado == '0':  # si trabaja en mas de un turno los sabados y en los feriados
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
								empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
								empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado == '1' and horarioAdicionalFeriado == '1':  # si no trabaja en mas de un turno los sabados y en los feriados
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado == '1' and horarioAdicionalFeriado == '0':  # si no trabaja en mas de un turno los sabados, pero si los feriados
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
								empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.save()
								return HttpResponseRedirect('/')
						elif trabajaFinde == '1' and horarioFeriado == '1':  # trabaja el domingo, pero no los feriados
							if horarioAdicionalDomingo == '0':  # si trabaja en mas de un turno
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
								empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
								empleado.save()
								return HttpResponseRedirect('/')
							else:
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.save()
								return HttpResponseRedirect('/')

						elif trabajaFinde == '1' and horarioFeriado == '0':  # trabaja el domingo y los feriados
							if horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '1':  # si trabaja en mas de un turno los domingos, pero no los feriados
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
								empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '0':  # si trabaja en mas de un turno los domingos y los feriados
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
								empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
								empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '1':  # si no trabaja en mas de un turno los domingos y los feriados
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '0':  # si no trabaja en mas de un turno los domingos, pero si los feriados
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
								empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.save()
								return HttpResponseRedirect('/')
						elif trabajaFinde == '2' and horarioFeriado == '1':  # trabaja el sabado y el domingo, pero no los feriados
							if horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '1':  # si trabaja en mas de un turno el sabado
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
								empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '1':
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalDomingo == '0' and horarioAdicionalSabado == '1':  # si trabaja en mas de un turno el domingo
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
								empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalDomingo == '0' and horarioAdicionalSabado == '0':  # si trabaja en mas de un turno el sabado y domingo
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
								empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
								empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
								empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
								empleado.save()
								return HttpResponseRedirect('/')
						elif trabajaFinde == '2' and horarioFeriado == '0':  # trabaja el sabado y el domingo, y tambien los feriados
							if horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '1 ' and horarioAdicionalFeriado == '1':  # si trabaja en mas de un turno el sabado, pero no los feriados y los domingos
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
								empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '1':  # si no trabaja en mas de un turno los sabados y feriados, pero si los domingos
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
								empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '1':  # si trabaja en mas de un turno el domingo y los sabados, pero no los feriados
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
								empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
								empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '0':  # si trabaja en mas de un turno los domingos y feriados, pero no los sabados
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
								empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
								empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '1':  # si no trabaja en mas de un turno
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '0' and horarioAdicionalFeriado == '0':  # si trabaja en mas de un turno
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
								empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
								empleado.horarioDomingoAdicionalInicio = horarioAdicionalDomingoInicio
								empleado.horarioDomingoAdicionalFin = horarioAdicionalDomingoFin
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
								empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado == '1' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '0':  # si trabaja en mas de un turno los feriados, pero no los sabados y domingos
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
								empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado == '0' and horarioAdicionalDomingo == '1' and horarioAdicionalFeriado == '0':  # si trabaja en mas de un turno los domingos, pero no los sabados y feriados
								empleado.horarioDomingoFin = horarioDomingoFin
								empleado.horarioDomingoInicio = horarioDomingoInicio
								empleado.horarioSabadoInicio = horarioSabadoInicio
								empleado.horarioSabadoFin = horarioSabadoFin
								empleado.horarioSabadoAdicionalInicio = horarioAdicionalSabadoInicio
								empleado.horarioSabadoAdicionalFin = horarioAdicionalSabadoFin
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
								empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
								empleado.save()
								return HttpResponseRedirect('/')

						elif trabajaFinde == '3' and horarioFeriado == '0':  # si no trabaja sabado y domingo, pero si los feriados
							if horarioAdicionalFeriado == '1':  # si trabaja los feriados en un solo turno
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalFeriado == '0':  # si trabaja los feriados en mas de un turno
								empleado.horarioFeriadoInicio = horarioFeriadoInicio
								empleado.horarioFeriadoFin = horarioFeriadoFin
								empleado.horarioFeriadoAdicionalInicio = horarioAdicionalFeriadoInicio
								empleado.horarioFeriadoAdicionalFin = horarioAdicionalFeriadoFin
								empleado.save()
								return HttpResponseRedirect('/')

		else:
			context = {}
			return render(request, "modificarEmpleados.html", context)
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')		
		
def mostrarEmpleado(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			dato = request.POST['dato']
			if dato == '1':
				valor = request.POST['valor']
				consorcio = request.POST['consorcio']
			resultado = 0
			if resultado == 0:
				if dato == '1':  # MOSTRAR UNO ESPECIFICO

					if valor == '1':  # MOSTRAR DE LA ADMINISTRACION
						admin = Administracion.objects.get(id=1)
						empleado = Empleado.objects.all().filter(admin_id=admin.id)  # idAdministracion = 1
						return render_to_response('empleado.html', {'empleado': empleado},
												  context_instance=RequestContext(request))

					elif valor == '2':  # MOSTRAR DE UN CONSORCIO
						con = Consorcio.objects.filter(id=consorcio)  # Verifico si el consorcio existe
						if con.exists() == True:  # CONSORCIO EXISTENTE
							con = Consorcio.objects.get(id=consorcio)
							empleados = Empleado.objects.all().filter(consorcio_id=con.id)
							return render_to_response('empleados.html', {'empleado': empleados, 'con': con},
													  context_instance=RequestContext(request))
						else:
							context = {}
							return render(request, "mostrarEmpleado2.html", context)

				elif dato == '2':  # MOSTRAR TODOS
					listaempleado = Empleado.objects.all()
					listaconsorcios = Consorcio.objects.all()
					return render_to_response('mostrarEmpleados.html',
											  {'listaempleado': listaempleado, 'listaconsorcios': listaconsorcios},
											  context_instance=RequestContext(request))

		else:
			context = {}
			return render(request, "mostrarEmpleado.html", context)
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')	
		
def agregarEmpleado(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1	
			valor = request.POST['valor']
			consorcio = request.POST['consorcio']
			nombre = request.POST['nombre']
			apellido = request.POST['apellido']
			dni = request.POST['dni']
			cuil = request.POST['cuil']
			email = request.POST['email']
			nacionalidad = request.POST['nacionalidad']
			telFijo = request.POST['telFijo']
			celular = request.POST['celular']
			direccion = request.POST['direccion']
			localidad = request.POST['localidad']
			cp = request.POST['cp']
			trabajaSemana = request.POST['trabajaSemana']
			trabajaFinde  = request.POST['trabajaFinde']
			fechaNacimiento = request.POST['fechaNacimiento']
			fechaIngreso = request.POST['fechaIngreso']
			funcion = request.POST['funcion']
			categoria = request.POST['categoria']
			estadocivil = request.POST['estadocivil']
			estudios = request.POST['estudios']
			horarioFeriado = request.POST['horarioFeriado']
			observaciones = request.POST['observaciones']
			if trabajaSemana=='0':#si trabaja en la semana
				horarioInicio = request.POST['horarioInicio']
				horarioFin = request.POST['horarioFin']
				horarioAdicional = request.POST['horarioAdicional']
				if horarioAdicional=='0':#si trabaja en mas de un turno
					horarioAdicionalSemanalInicio = request.POST['horarioAdicionalSemanalInicio']
					horarioAdicionalSemanalFin = request.POST['horarioAdicionalSemanalFin']
			if trabajaFinde=='0':#trabaja el sabado
				horarioSabadoInicio = request.POST['horarioSabadoInicio']
				horarioSabadoFin = request.POST['horarioSabadoFin']
				horarioAdicionalSabado = request.POST['horarioAdicionalSabado'] 
				if horarioAdicionalSabado=='0':#si trabaja en mas de un turno
					horarioAdicionalSabadoInicio = request.POST['horarioAdicionalSabadoInicio']
					horarioAdicionalSabadoFin = request.POST['horarioAdicionalSabadoFin']
			if trabajaFinde=='1':#si trabaja el domingo
				horarioDomingoInicio = request.POST['horarioDomingoInicio']
				horarioDomingoFin = request.POST['horarioDomingoFin']
				horarioAdicionalDomingo = request.POST['horarioAdicionalDomingo']
				if horarioAdicionalDomingo=='0':#si trabaja en mas de un turno
					horarioAdicionalDomingoInicio = request.POST['horarioAdicionalDomingoInicio']
					horarioAdicionalDomingoFin = request.POST['horarioAdicionalDomingoFin']
			if trabajaFinde=='2':#si trabaja sabado y domingo
				horarioSabadoInicio = request.POST['horarioSabadoInicio']
				horarioSabadoFin = request.POST['horarioSabadoFin']
				horarioAdicionalSabado = request.POST['horarioAdicionalSabado'] 
				if horarioAdicionalSabado=='0':#si trabaja en mas de un turno
					horarioAdicionalSabadoInicio = request.POST['horarioAdicionalSabadoInicio']
					horarioAdicionalSabadoFin = request.POST['horarioAdicionalSabadoFin']
				horarioDomingoInicio = request.POST['horarioDomingoInicio']
				horarioDomingoFin = request.POST['horarioDomingoFin']
				horarioAdicionalDomingo = request.POST['horarioAdicionalDomingo']
				if horarioAdicionalDomingo=='0':#si trabaja en mas de un turno
					horarioAdicionalDomingoInicio = request.POST['horarioAdicionalDomingoInicio']
					horarioAdicionalDomingoFin = request.POST['horarioAdicionalDomingoFin']
				if horarioFeriado == '0':#si trabaja los feriados
					horarioFeriadoInicio = request.POST['horarioFeriadoInicio']
					horarioFeriadoFin = request.POST['horarioFeriadoFin']
					horarioAdicionalFeriado = request.POST['horarioAdicionalFeriado']
					if horarioAdicionalFeriado == '0':#si trabaja en mas de un turno
						horarioAdicionalFeriadoInicio = request.POST['horarioAdicionalFeriadoInicio']
						horarioAdicionalFeriadoFin = request.POST['horarioAdicionalFeriadoFin']
			resultado = 0
			if resultado==0:
				if valor=='1': # PARA LA ADMINISTRACION
					admin = Administracion.objects.get(id=1)
					if trabajaSemana=='0' and horarioFeriado == '1':#si trabaja en la semana, pero no trabaja feriados
						if horarioAdicional=='0':#si tiene horario adicional
							empleado = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, observaciones=observaciones) #idAdministracion = 1
							empleado.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='1':#si no tiene horario adicional
							empleado1 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones) #idAdministracion = 1
							empleado1.save()
							return HttpResponseRedirect('/')
					elif trabajaSemana=='0' and horarioFeriado == '0':#si trabaja en la semana y trabaja feriados
						if horarioAdicional=='0' and horarioAdicionalFeriado=='1':#si tiene horario adicional, pero no los feriados
							empleado2 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado2.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana y tambien en los feriados
							empleado3 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado3.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana y en los feriados
							empleado4 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado4.save()
							return HttpResponseRedirect('/')		
						elif horarioAdicional=='1' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana, pero si en los feriados
							empleado5 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado5.save()
							return HttpResponseRedirect('/')
					elif trabajaSemana=='0' and trabajaFinde == '0' and horarioFeriado=='1':#si trabaja en la semana y trabaja los sabados
						if horarioAdicional=='0' and horarioAdicionalSabado=='1':#si tiene horario adicional, pero no los sabados
							empleado60 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, observaciones=observaciones) #idAdministracion = 1
							empleado60.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalSabado=='0':#si tiene horario adicional en la semana y tambien los sabados
							empleado61 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado61.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalSabado=='1':#si no tiene horario adicional en la semana y los sabados
							empleado62 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, observaciones=observaciones) #idAdministracion = 1
							empleado62.save()
							return HttpResponseRedirect('/')		
						elif horarioAdicional=='1' and horarioAdicionalSabado=='0':#si no tiene horario adicional en la semana, pero si los sabados
							empleado63 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado63.save()
							return HttpResponseRedirect('/')
					#Trabaja Feriados ademas de los dias en los que trabaja
					elif trabajaSemana=='0' and trabajaFinde == '0' and horarioFeriado=='0':#si trabaja en la semana y trabaja los sabados
						if horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalFeriado=='1': #si tiene horario adicional solo en la semana, pero no los sabados y feriados
							empleado92 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioFeriadoInicio=horarioFeriadoInicio,
							horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado92.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalFeriado=='1':#si tiene horario adicional en la semana y tambien los sabados, pero no los feriados
							empleado93 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin,
							horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado93.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana y los sabados y feriados
							empleado94 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioFeriadoInicio=horarioFeriadoInicio,
							horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado94.save()
							return HttpResponseRedirect('/')		
						elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana y en los feriados, pero si los sabados
							empleado95 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
							horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado95.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalFeriado=='0': #si tiene horario adicional en la semana y en los feriados, pero no los sabados
							empleado96 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin,
							horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado96.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana, los sabados y tambien en los feriados
							empleado97 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
							horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin,
							horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado97.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana y los sabados, pero si los feriados
							empleado98 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin,
							horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado98.save()
							return HttpResponseRedirect('/')		
						elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana, pero si los sabados y feriados
							empleado99 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin,
							horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin,
							horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado99.save()
							return HttpResponseRedirect('/')			
					elif trabajaSemana=='0' and trabajaFinde == '1' and horarioFeriado=='1':#si trabaja en la semana y trabaja los domingos
						if horarioAdicional=='0' and horarioAdicionalDomingo=='1':#si tiene horario adicional, pero no los sabados
							empleado64 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, observaciones=observaciones) #idAdministracion = 1
							empleado64.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalDomingo=='0':#si tiene horario adicional en la semana y tambien los domingos
							empleado65 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
							empleado65.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalDomingo=='1':#si no tiene horario adicional en la semana y los domingos
							empleado66 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, observaciones=observaciones) #idAdministracion = 1
							empleado66.save()
							return HttpResponseRedirect('/')		
						elif horarioAdicional=='1' and horarioAdicionalDomingo=='0':#si no tiene horario adicional en la semana, pero si los domingos
							empleado67 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
							empleado67.save()
							return HttpResponseRedirect('/')
					#Ademas de los dias en los que trabaja tambien lo hace los feriados
					elif trabajaSemana=='0' and trabajaFinde == '1' and horarioFeriado=='0':#si trabaja en la semana y trabaja los domingos
						if horarioAdicional=='0' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='1':#si tiene horario adicional en la semana, pero no los sabados y feriados
							empleado111 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado111.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si tiene horario adicional en la semana y tambien los domingos, pero no los feriados
							empleado112 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, 
							horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado112.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana, los domingos y feriados
							empleado113 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado113.save()
							return HttpResponseRedirect('/')		
						elif horarioAdicional=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana y los feriados, pero si los domingos
							empleado114 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, 
							horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado114.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana y los feriados, pero no los domingos
							empleado115 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, 
							horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado115.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana y tambien los domingos y feriados
							empleado116 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, 
							horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado116.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana y los domingos, pero si los feriados
							empleado117 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, 
							horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado117.save()
							return HttpResponseRedirect('/')		
						elif horarioAdicional=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana, pero si los domingos y feriados
							empleado118 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, 
							horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, 
							horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado118.save()
							return HttpResponseRedirect('/')	
									
					elif trabajaSemana=='0' and trabajaFinde == '2' and horarioFeriado=='1':#si trabaja en la semana y trabaja los sabados y domingos, pero no los feriados
						if horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1':#si tiene horario adicional en la semana, pero no los sabados y domingos
							empleado68 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, observaciones=observaciones) #idAdministracion = 1
							empleado68.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0':#si tiene horario adicional en la semana y tambien los sabados y domingos
							empleado69 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
							empleado69.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0':#si no tiene horario adicional en la semana y los sabados, pero si los domingos
							empleado70 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin,
							horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
							empleado70.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0':#si no tiene horario adicional en la semana, pero si los sabados y domingos
							empleado71 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
							empleado71.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1':#si no tiene horario adicional en la semana y domingos, pero si los sabados 
							empleado72 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin,
							horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado72.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0':#si tiene horario adicional en la semana y los domingos, pero no los sabados 
							empleado73 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, 
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin,observaciones=observaciones) #idAdministracion = 1
							empleado73.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1':#si no tiene horario adicional en la semana y tambien los sabados y domingos
							empleado74 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, observaciones=observaciones) #idAdministracion = 1
							empleado74.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1':#si tiene horario adicional en la semana y sabados, pero no los domingos 
							empleado75 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, 
							horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado75.save()
							return HttpResponseRedirect('/')			
					elif trabajaSemana=='0' and trabajaFinde == '2' and horarioFeriado=='0':#si trabaja en la semana y trabaja los sabados y domingos y los feriados
						#No Trabaja adicional los feriados--------------------------------------------------------------------------------------------
						if horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='1':#si tiene horario adicional en la semana, pero no los sabados y domingos
							empleado76 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoFin=horarioFeriadoFin,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, observaciones=observaciones) #idAdministracion = 1
							empleado76.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si tiene horario adicional en la semana y tambien los sabados y domingos
							empleado77 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoFin=horarioFeriadoFin,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
							empleado77.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana y los sabados, pero si los domingos
							empleado78 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin,
							horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
							empleado78.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana, pero si los sabados y domingos
							empleado79 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
							empleado79.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana y domingos, pero si los sabados 
							empleado80 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin,
							horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado80.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si tiene horario adicional en la semana y los domingos, pero no los sabados 
							empleado81 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio, horarioFeriadoFin=horarioFeriadoFin,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, 
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin,observaciones=observaciones) #idAdministracion = 1
							empleado81.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana y tambien los sabados y domingos
							empleado82 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, observaciones=observaciones) #idAdministracion = 1
							empleado82.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='1':#si tiene horario adicional en la semana y sabados, pero no los domingos 
							empleado83 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoFin=horarioFeriadoFin,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, 
							horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones) #idAdministracion = 1
							empleado83.save()
							return HttpResponseRedirect('/')
						#Trabaja adicional los feriados--------------------------------------------------------------------------------------------	
						elif horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana, pero no los sabados y domingos
							empleado84 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoFin=horarioFeriadoFin,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, observaciones=observaciones,
							horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
							empleado84.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana y tambien los sabados y domingos
							empleado85 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoFin=horarioFeriadoFin,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones,
							horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
							empleado85.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana y los sabados, pero si los domingos
							empleado86 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin,
							horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones, 
							horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
							empleado86.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana, pero si los sabados y domingos
							empleado87 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones, 
							horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
							empleado87.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana y domingos, pero si los sabados 
							empleado88 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin,
							horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones,
							horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
							empleado88.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana y los domingos, pero no los sabados 
							empleado89 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio, horarioFeriadoFin=horarioFeriadoFin,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, 
							horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin,
							observaciones=observaciones, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
							empleado89.save()
							return HttpResponseRedirect('/')	
						elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana y tambien los sabados y domingos
							empleado90 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, 
							observaciones=observaciones, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
							empleado90.save()
							return HttpResponseRedirect('/')
						elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana y sabados, pero no los domingos 
							empleado91 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
							telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
							horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoFin=horarioFeriadoFin,
							horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioFeriadoInicio=horarioFeriadoInicio, 
							horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, 
							horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones,
							horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
							empleado91.save()
							return HttpResponseRedirect('/')	
							
					elif trabajaSemana=='1' and horarioFeriado == '1':#si no trabaja en la semana y no tampoco los feriados		
						if trabajaFinde=='0':#trabaja el sabado
							if horarioAdicionalSabado=='0':#si trabaja en mas de un turno
								empleado6 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, funcion=funcion, estadoCivil=estadocivil,
								categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado6.save()
								return HttpResponseRedirect('/')
							else: 
								empleado7 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
								horarioSabadoFin=horarioSabadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado7.save()
								return HttpResponseRedirect('/')
						elif trabajaFinde=='1':#trabaja el domingo
							if horarioAdicionalDomingo=='0':#si trabaja en mas de un turno
								empleado8 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, funcion=funcion, estadoCivil=estadocivil,
								categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado8.save()
								return HttpResponseRedirect('/')
							else: 
								empleado9 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado9.save()
								return HttpResponseRedirect('/')
						elif trabajaFinde=='2':#trabaja el sabado y el domingo
							if horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1':#si trabaja en mas de un turno el sabado
								empleado10 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, funcion=funcion, estadoCivil=estadocivil,
								categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado10.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1': 
								empleado11 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
								horarioSabadoFin=horarioSabadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado11.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalDomingo=='0' and horarioAdicionalSabado=='1':#si trabaja en mas de un turno el domingo
								empleado12 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, funcion=funcion, estadoCivil=estadocivil,
								categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado12.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalDomingo=='0' and horarioAdicionalSabado=='0':
								empleado13 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin,
								horarioSabadoInicio=horarioSabadoInicio,horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin,
								funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado13.save()
								return HttpResponseRedirect('/')
						#elif trabajaFinde=='3':#si no trabaja sabado y domingo
						#	return HttpResponseRedirect('/')
					elif trabajaSemana=='1' and horarioFeriado == '0':#si no trabaja en la semana, pero si los feriados		
						if trabajaFinde=='0' and horarioFeriado == '1':#trabaja el sabado, pero no los feriados
							if horarioAdicionalSabado=='0':#si trabaja en mas de un turno
								empleado14 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, funcion=funcion, estadoCivil=estadocivil,
								categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado14.save()
								return HttpResponseRedirect('/')
							else: 
								empleado15 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
								horarioSabadoFin=horarioSabadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado15.save()
								return HttpResponseRedirect('/')
						elif trabajaFinde=='0' and horarioFeriado == '0':#trabaja el sabado y los feriados
							if horarioAdicionalSabado=='0' and horarioAdicionalFeriado=='1':#si trabaja en mas de un turno los sabados, pero no los feriados
								empleado16 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, funcion=funcion, estadoCivil=estadocivil,
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado16.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado=='0' and horarioAdicionalFeriado=='0':#si trabaja en mas de un turno los sabados y en los feriados
								empleado17 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, funcion=funcion, estadoCivil=estadocivil,
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin,
								categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado17.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicionalSabado=='1' and horarioAdicionalFeriado=='1':#si no trabaja en mas de un turno los sabados y en los feriados 
								empleado18 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
								horarioSabadoFin=horarioSabadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado18.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado=='1' and horarioAdicionalFeriado=='0':#si no trabaja en mas de un turno los sabados, pero si los feriados 
								empleado19 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin,
								horarioSabadoFin=horarioSabadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado19.save()
								return HttpResponseRedirect('/')		
						elif trabajaFinde=='1' and horarioFeriado == '1':#trabaja el domingo, pero no los feriados
							if horarioAdicionalDomingo=='0':#si trabaja en mas de un turno
								empleado20 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, funcion=funcion, estadoCivil=estadocivil,
								categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado20.save()
								return HttpResponseRedirect('/')
							else: 
								empleado21 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado21.save()
								return HttpResponseRedirect('/')
					
						elif trabajaFinde=='1' and horarioFeriado == '0':#trabaja el domingo y los feriados
							if horarioAdicionalDomingo=='0'  and horarioAdicionalFeriado=='1':#si trabaja en mas de un turno los domingos, pero no los feriados
								empleado26 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, funcion=funcion, estadoCivil=estadocivil,
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado26.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalDomingo=='0'  and horarioAdicionalFeriado=='0':#si trabaja en mas de un turno los domingos y los feriados
								empleado27 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, funcion=funcion, estadoCivil=estadocivil,
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones,
								categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento)
								empleado27.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicionalDomingo=='1'  and horarioAdicionalFeriado=='1': #si no trabaja en mas de un turno los domingos y los feriados
								empleado28 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, 
								horarioDomingoInicio=horarioDomingoInicio, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado28.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalDomingo=='1'  and horarioAdicionalFeriado=='0': #si no trabaja en mas de un turno los domingos, pero si los feriados
								empleado29 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin,
								horarioDomingoInicio=horarioDomingoInicio, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado29.save()
								return HttpResponseRedirect('/')		
						elif trabajaFinde=='2' and horarioFeriado=='1':#trabaja el sabado y el domingo, pero no los feriados
							if horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1':#si trabaja en mas de un turno el sabado
								empleado30 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, funcion=funcion, estadoCivil=estadocivil,
								categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioDomingoFin=horarioDomingoFin, horarioDomingoInicio=horarioDomingoInicio, observaciones=observaciones)
								empleado30.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1': 
								empleado31 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
								horarioSabadoFin=horarioSabadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, 
								horarioDomingoFin=horarioDomingoFin, horarioDomingoInicio=horarioDomingoInicio, observaciones=observaciones)
								empleado31.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalDomingo=='0' and horarioAdicionalSabado=='1':#si trabaja en mas de un turno el domingo
								empleado32 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, funcion=funcion, estadoCivil=estadocivil,
								categoriaFuncion=categoria, horarioSabadoFin=horarioSabadoFin, fechaNacimiento=fechaNacimiento, horarioSabadoInicio=horarioSabadoInicio, observaciones=observaciones)
								empleado32.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalDomingo=='0' and horarioAdicionalSabado=='0': #si trabaja en mas de un turno el sabado y domingo
								empleado33 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, funcion=funcion, horarioSabadoFin=horarioSabadoFin,  estadoCivil=estadocivil, categoriaFuncion=categoria,
								horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin,	horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, 
								horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, fechaNacimiento=fechaNacimiento, horarioSabadoInicio=horarioSabadoInicio, observaciones=observaciones)
								empleado33.save()
								return HttpResponseRedirect('/')
						elif trabajaFinde=='2' and horarioFeriado=='0':#trabaja el sabado y el domingo, y tambien los feriados
							if horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1 ' and horarioAdicionalFeriado=='1':#si trabaja en mas de un turno el sabado, pero no los feriados y los domingos
								empleado34 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, funcion=funcion, estadoCivil=estadocivil,
								categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioDomingoFin=horarioDomingoFin, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin,  
								horarioDomingoInicio=horarioDomingoInicio, observaciones=observaciones)
								empleado34.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si no trabaja en mas de un turno los sabados y feriados, pero si los domingos
								empleado35 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
								horarioSabadoFin=horarioSabadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones,
								horarioDomingoFin=horarioDomingoFin, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin,
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin)
								empleado35.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si trabaja en mas de un turno el domingo y los sabados, pero no los feriados 
								empleado36 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, funcion=funcion, estadoCivil=estadocivil,
								categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones,
								horarioSabadoInicio=horarioSabadoInicio, horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, 
								horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin)
								empleado36.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si trabaja en mas de un turno los domingos y feriados, pero no los sabados
								empleado37 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoFin=horarioSabadoFin, funcion=funcion, 
								horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin,
								estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado37.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='1':#si no trabaja en mas de un turno
								empleado38 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, funcion=funcion, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoFin=horarioSabadoFin, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioFeriadoFin=horarioFeriadoFin, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado38.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si trabaja en mas de un turno
								empleado39 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoFin=horarioSabadoFin,  horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, 
								horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio,  horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin,
								funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado39.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si trabaja en mas de un turno los feriados, pero no los sabados y domingos 
								empleado40 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, funcion=funcion, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoFin=horarioSabadoFin, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, 
								horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado40.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si trabaja en mas de un turno los domingos, pero no los sabados y feriados
								empleado41 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, 
								horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, 
								horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado41.save()
								return HttpResponseRedirect('/')	
			
						elif trabajaFinde=='3' and horarioFeriado=='0':#si no trabaja sabado y domingo, pero si los feriados
							if horarioAdicionalFeriado=='1':#si trabaja los feriados en un solo turno
								empleado42 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, 
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, 
								fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado42.save()
								return HttpResponseRedirect('/')
							elif horarioAdicionalFeriado=='0':#si trabaja los feriados en mas de un turno
								empleado43 = Empleado.objects.create(admin_id=admin.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, 
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, 
								horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
								empleado43.save()
								return HttpResponseRedirect('/')			
						
				elif valor=='2': #PARA EL CONSORCIO
					consorcios1 = Consorcio.objects.filter(id = consorcio) #Verifico si el consorcio existe para modificarlo
					if consorcios1.exists() == True: #CONSORCIO EXISTENTE
						con = Consorcio.objects.get(id=consorcio)
						if trabajaSemana=='0' and horarioFeriado == '1':#si trabaja en la semana, pero no trabaja feriados
							if horarioAdicional=='0':#si tiene horario adicional
								empleado = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, observaciones=observaciones) #idAdministracion = 1
								empleado.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='1':#si no tiene horario adicional
								empleado1 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones) #idAdministracion = 1
								empleado1.save()
								return HttpResponseRedirect('/')
						elif trabajaSemana=='0' and horarioFeriado == '0':#si trabaja en la semana y trabaja feriados
							if horarioAdicional=='0' and horarioAdicionalFeriado=='1':#si tiene horario adicional, pero no los feriados
								empleado2 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado2.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana y tambien en los feriados
								empleado3 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado3.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana y en los feriados
								empleado4 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado4.save()
								return HttpResponseRedirect('/')		
							elif horarioAdicional=='1' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana, pero si en los feriados
								empleado5 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado5.save()
								return HttpResponseRedirect('/')
						elif trabajaSemana=='0' and trabajaFinde == '0' and horarioFeriado=='1':#si trabaja en la semana y trabaja los sabados
							if horarioAdicional=='0' and horarioAdicionalSabado=='1':#si tiene horario adicional, pero no los sabados
								empleado60 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, observaciones=observaciones) #idAdministracion = 1
								empleado60.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalSabado=='0':#si tiene horario adicional en la semana y tambien los sabados
								empleado61 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado61.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalSabado=='1':#si no tiene horario adicional en la semana y los sabados
								empleado62 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, observaciones=observaciones) #idAdministracion = 1
								empleado62.save()
								return HttpResponseRedirect('/')		
							elif horarioAdicional=='1' and horarioAdicionalSabado=='0':#si no tiene horario adicional en la semana, pero si los sabados
								empleado63 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado63.save()
								return HttpResponseRedirect('/')
					#Trabaja Feriados ademas de los dias en los que trabaja
						elif trabajaSemana=='0' and trabajaFinde == '0' and horarioFeriado=='0':#si trabaja en la semana y trabaja los sabados
							if horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalFeriado=='1': #si tiene horario adicional solo en la semana, pero no los sabados y feriados
								empleado92 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioFeriadoInicio=horarioFeriadoInicio,
								horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado92.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalFeriado=='1':#si tiene horario adicional en la semana y tambien los sabados, pero no los feriados
								empleado93 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin,
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado93.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana y los sabados y feriados
								empleado94 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioFeriadoInicio=horarioFeriadoInicio,
								horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado94.save()
								return HttpResponseRedirect('/')		
							elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana y en los feriados, pero si los sabados
								empleado95 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado95.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalFeriado=='0': #si tiene horario adicional en la semana y en los feriados, pero no los sabados
								empleado96 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin,
								horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado96.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana, los sabados y tambien en los feriados
								empleado97 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin,
								horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado97.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana y los sabados, pero si los feriados
								empleado98 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin,
								horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado98.save()
								return HttpResponseRedirect('/')		
							elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana, pero si los sabados y feriados
								empleado99 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin,
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin,
								horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado99.save()
								return HttpResponseRedirect('/')			
						elif trabajaSemana=='0' and trabajaFinde == '1' and horarioFeriado=='1':#si trabaja en la semana y trabaja los domingos
							if horarioAdicional=='0' and horarioAdicionalDomingo=='1':#si tiene horario adicional, pero no los sabados
								empleado64 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, observaciones=observaciones) #idAdministracion = 1
								empleado64.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalDomingo=='0':#si tiene horario adicional en la semana y tambien los domingos
								empleado65 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
								empleado65.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalDomingo=='1':#si no tiene horario adicional en la semana y los domingos
								empleado66 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, observaciones=observaciones) #idAdministracion = 1
								empleado66.save()
								return HttpResponseRedirect('/')		
							elif horarioAdicional=='1' and horarioAdicionalDomingo=='0':#si no tiene horario adicional en la semana, pero si los domingos
								empleado67 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
								empleado67.save()
								return HttpResponseRedirect('/')
					#Ademas de los dias en los que trabaja tambien lo hace los feriados
						elif trabajaSemana=='0' and trabajaFinde == '1' and horarioFeriado=='0':#si trabaja en la semana y trabaja los domingos
							if horarioAdicional=='0' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='1':#si tiene horario adicional en la semana, pero no los sabados y feriados
								empleado111 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado111.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si tiene horario adicional en la semana y tambien los domingos, pero no los feriados
								empleado112 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, 
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado112.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana, los domingos y feriados
								empleado113 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado113.save()
								return HttpResponseRedirect('/')		
							elif horarioAdicional=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana y los feriados, pero si los domingos
								empleado114 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, 
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado114.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana y los feriados, pero no los domingos
								empleado115 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, 
								horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado115.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana y tambien los domingos y feriados
								empleado116 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, 
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado116.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana y los domingos, pero si los feriados
								empleado117 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, 
								horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado117.save()
								return HttpResponseRedirect('/')		
							elif horarioAdicional=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana, pero si los domingos y feriados
								empleado118 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, 
								horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, 
								horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado118.save()
								return HttpResponseRedirect('/')	
									
						elif trabajaSemana=='0' and trabajaFinde == '2' and horarioFeriado=='1':#si trabaja en la semana y trabaja los sabados y domingos, pero no los feriados
							if horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1':#si tiene horario adicional en la semana, pero no los sabados y domingos
								empleado68 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, observaciones=observaciones) #idAdministracion = 1
								empleado68.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0':#si tiene horario adicional en la semana y tambien los sabados y domingos
								empleado69 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
								empleado69.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0':#si no tiene horario adicional en la semana y los sabados, pero si los domingos
								empleado70 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
								empleado70.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0':#si no tiene horario adicional en la semana, pero si los sabados y domingos
								empleado71 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
								empleado71.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1':#si no tiene horario adicional en la semana y domingos, pero si los sabados 
								empleado72 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin,
								horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado72.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0':#si tiene horario adicional en la semana y los domingos, pero no los sabados 
								empleado73 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, 
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin,observaciones=observaciones) #idAdministracion = 1
								empleado73.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1':#si no tiene horario adicional en la semana y tambien los sabados y domingos
								empleado74 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, observaciones=observaciones) #idAdministracion = 1
								empleado74.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1':#si tiene horario adicional en la semana y sabados, pero no los domingos 
								empleado75 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin,
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, 
								horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado75.save()
								return HttpResponseRedirect('/')			
						elif trabajaSemana=='0' and trabajaFinde == '2' and horarioFeriado=='0':#si trabaja en la semana y trabaja los sabados y domingos y los feriados
						#No Trabaja adicional los feriados--------------------------------------------------------------------------------------------
							if horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='1':#si tiene horario adicional en la semana, pero no los sabados y domingos
								empleado76 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoFin=horarioFeriadoFin,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, observaciones=observaciones) #idAdministracion = 1
								empleado76.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si tiene horario adicional en la semana y tambien los sabados y domingos
								empleado77 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoFin=horarioFeriadoFin,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
								empleado77.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana y los sabados, pero si los domingos
								empleado78 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
								empleado78.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana, pero si los sabados y domingos
								empleado79 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones) #idAdministracion = 1
								empleado79.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana y domingos, pero si los sabados 
								empleado80 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin,
								horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado80.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si tiene horario adicional en la semana y los domingos, pero no los sabados 
								empleado81 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio, horarioFeriadoFin=horarioFeriadoFin,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, 
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin,observaciones=observaciones) #idAdministracion = 1
								empleado81.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='1':#si no tiene horario adicional en la semana y tambien los sabados y domingos
								empleado82 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, observaciones=observaciones) #idAdministracion = 1
								empleado82.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='1':#si tiene horario adicional en la semana y sabados, pero no los domingos 
								empleado83 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoFin=horarioFeriadoFin,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, 
								horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones) #idAdministracion = 1
								empleado83.save()
								return HttpResponseRedirect('/')
						#Trabaja adicional los feriados--------------------------------------------------------------------------------------------	
							elif horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana, pero no los sabados y domingos
								empleado84 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoFin=horarioFeriadoFin,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, observaciones=observaciones,
								horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
								empleado84.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana y tambien los sabados y domingos
								empleado85 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoFin=horarioFeriadoFin,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones,
								horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
								empleado85.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana y los sabados, pero si los domingos
								empleado86 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin,
								horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones, 
								horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
								empleado86.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana, pero si los sabados y domingos
								empleado87 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, 
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, observaciones=observaciones, 
								horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
								empleado87.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='1' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana y domingos, pero si los sabados 
								empleado88 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin,
								horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones,
								horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
								empleado88.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana y los domingos, pero no los sabados 
								empleado89 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio, horarioFeriadoFin=horarioFeriadoFin,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, 
								horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin,
								observaciones=observaciones, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
								empleado89.save()
								return HttpResponseRedirect('/')	
							elif horarioAdicional=='1' and horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si no tiene horario adicional en la semana y tambien los sabados y domingos
								empleado90 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, horarioFeriadoFin=horarioFeriadoFin,
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, 
								observaciones=observaciones, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
								empleado90.save()
								return HttpResponseRedirect('/')
							elif horarioAdicional=='0' and horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si tiene horario adicional en la semana y sabados, pero no los domingos 
								empleado91 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
								telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSemanalInicio=horarioInicio,
								horarioSemanalFin=horarioFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioFeriadoFin=horarioFeriadoFin,
								horarioSemanalAdicionalInicio=horarioAdicionalSemanalInicio, horarioSemanalAdicionalFin=horarioAdicionalSemanalFin, horarioFeriadoInicio=horarioFeriadoInicio, 
								horarioSabadoFin=horarioSabadoFin, horarioSabadoInicio=horarioSabadoInicio, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoFin=horarioDomingoFin, 
								horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, observaciones=observaciones,
								horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin) #idAdministracion = 1
								empleado91.save()
								return HttpResponseRedirect('/')	
							
						elif trabajaSemana=='1' and horarioFeriado == '1':#si no trabaja en la semana y no tampoco los feriados		
							if trabajaFinde=='0':#trabaja el sabado
								if horarioAdicionalSabado=='0':#si trabaja en mas de un turno
									empleado6 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
									horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, funcion=funcion, estadoCivil=estadocivil,
									categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado6.save()
									return HttpResponseRedirect('/')
								else: 
									empleado7 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
									horarioSabadoFin=horarioSabadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado7.save()
									return HttpResponseRedirect('/')
							elif trabajaFinde=='1':#trabaja el domingo
								if horarioAdicionalDomingo=='0':#si trabaja en mas de un turno
									empleado8 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, funcion=funcion, estadoCivil=estadocivil,
									categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado8.save()
									return HttpResponseRedirect('/')
								else: 
									empleado9 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado9.save()
									return HttpResponseRedirect('/')
							elif trabajaFinde=='2':#trabaja el sabado y el domingo
								if horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1':#si trabaja en mas de un turno el sabado
									empleado10 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
									horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, funcion=funcion, estadoCivil=estadocivil,
									categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado10.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1': 
									empleado11 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
									horarioSabadoFin=horarioSabadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado11.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalDomingo=='0' and horarioAdicionalSabado=='1':#si trabaja en mas de un turno el domingo
									empleado12 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, funcion=funcion, estadoCivil=estadocivil,
									categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado12.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalDomingo=='0' and horarioAdicionalSabado=='0':
									empleado13 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin,
									horarioSabadoInicio=horarioSabadoInicio,horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin,
									funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado13.save()
									return HttpResponseRedirect('/')
							#elif trabajaFinde=='3':#si no trabaja sabado y domingo
							#	return HttpResponseRedirect('/')
						elif trabajaSemana=='1' and horarioFeriado == '0':#si no trabaja en la semana, pero si los feriados		
							if trabajaFinde=='0' and horarioFeriado == '1':#trabaja el sabado, pero no los feriados
								if horarioAdicionalSabado=='0':#si trabaja en mas de un turno
									empleado14 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
									horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, funcion=funcion, estadoCivil=estadocivil,
									categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado14.save()
									return HttpResponseRedirect('/')
								else: 
									empleado15 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
									horarioSabadoFin=horarioSabadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado15.save()
									return HttpResponseRedirect('/')
							elif trabajaFinde=='0' and horarioFeriado == '0':#trabaja el sabado y los feriados
								if horarioAdicionalSabado=='0' and horarioAdicionalFeriado=='1':#si trabaja en mas de un turno los sabados, pero no los feriados
									empleado16 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
									horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, funcion=funcion, estadoCivil=estadocivil,
									horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado16.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalSabado=='0' and horarioAdicionalFeriado=='0':#si trabaja en mas de un turno los sabados y en los feriados
									empleado17 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
									horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, funcion=funcion, estadoCivil=estadocivil,
									horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin,
									categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado17.save()
									return HttpResponseRedirect('/')	
								elif horarioAdicionalSabado=='1' and horarioAdicionalFeriado=='1':#si no trabaja en mas de un turno los sabados y en los feriados 
									empleado18 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
									horarioSabadoFin=horarioSabadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado18.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalSabado=='1' and horarioAdicionalFeriado=='0':#si no trabaja en mas de un turno los sabados, pero si los feriados 
									empleado19 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
									horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin,
									horarioSabadoFin=horarioSabadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado19.save()
									return HttpResponseRedirect('/')		
							elif trabajaFinde=='1' and horarioFeriado == '1':#trabaja el domingo, pero no los feriados
								if horarioAdicionalDomingo=='0':#si trabaja en mas de un turno
									empleado20 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, funcion=funcion, estadoCivil=estadocivil,
									categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado20.save()
									return HttpResponseRedirect('/')
								else: 
									empleado21 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado21.save()
									return HttpResponseRedirect('/')
					
							elif trabajaFinde=='1' and horarioFeriado == '0':#trabaja el domingo y los feriados
								if horarioAdicionalDomingo=='0'  and horarioAdicionalFeriado=='1':#si trabaja en mas de un turno los domingos, pero no los feriados
									empleado26 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, funcion=funcion, estadoCivil=estadocivil,
									horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado26.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalDomingo=='0'  and horarioAdicionalFeriado=='0':#si trabaja en mas de un turno los domingos y los feriados
									empleado27 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, funcion=funcion, estadoCivil=estadocivil,
									horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, observaciones=observaciones,
									categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento)
									empleado27.save()
									return HttpResponseRedirect('/')	
								elif horarioAdicionalDomingo=='1'  and horarioAdicionalFeriado=='1': #si no trabaja en mas de un turno los domingos y los feriados
									empleado28 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, 
									horarioDomingoInicio=horarioDomingoInicio, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado28.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalDomingo=='1'  and horarioAdicionalFeriado=='0': #si no trabaja en mas de un turno los domingos, pero si los feriados
									empleado29 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin,
									horarioDomingoInicio=horarioDomingoInicio, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado29.save()
									return HttpResponseRedirect('/')		
							elif trabajaFinde=='2' and horarioFeriado=='1':#trabaja el sabado y el domingo, pero no los feriados
								if horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1':#si trabaja en mas de un turno el sabado
									empleado30 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
									horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, funcion=funcion, estadoCivil=estadocivil,
									categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioDomingoFin=horarioDomingoFin, horarioDomingoInicio=horarioDomingoInicio, observaciones=observaciones)
									empleado30.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1': 
									empleado31 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
									horarioSabadoFin=horarioSabadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, 
									horarioDomingoFin=horarioDomingoFin, horarioDomingoInicio=horarioDomingoInicio, observaciones=observaciones)
									empleado31.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalDomingo=='0' and horarioAdicionalSabado=='1':#si trabaja en mas de un turno el domingo
									empleado32 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, funcion=funcion, estadoCivil=estadocivil,
									categoriaFuncion=categoria, horarioSabadoFin=horarioSabadoFin, fechaNacimiento=fechaNacimiento, horarioSabadoInicio=horarioSabadoInicio, observaciones=observaciones)
									empleado32.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalDomingo=='0' and horarioAdicionalSabado=='0': #si trabaja en mas de un turno el sabado y domingo
									empleado33 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, funcion=funcion, horarioSabadoFin=horarioSabadoFin,  estadoCivil=estadocivil, categoriaFuncion=categoria,
									horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin,	horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, 
									horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, fechaNacimiento=fechaNacimiento, horarioSabadoInicio=horarioSabadoInicio, observaciones=observaciones)
									empleado33.save()
									return HttpResponseRedirect('/')
							elif trabajaFinde=='2' and horarioFeriado=='0':#trabaja el sabado y el domingo, y tambien los feriados
								if horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1 ' and horarioAdicionalFeriado=='1':#si trabaja en mas de un turno el sabado, pero no los feriados y los domingos
									empleado34 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
									horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, funcion=funcion, estadoCivil=estadocivil,
									categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, horarioDomingoFin=horarioDomingoFin, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin,  
									horarioDomingoInicio=horarioDomingoInicio, observaciones=observaciones)
									empleado34.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si no trabaja en mas de un turno los sabados y feriados, pero si los domingos
									empleado35 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioSabadoInicio=horarioSabadoInicio,
									horarioSabadoFin=horarioSabadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones,
									horarioDomingoFin=horarioDomingoFin, horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin,
									horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin)
									empleado35.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='1':#si trabaja en mas de un turno el domingo y los sabados, pero no los feriados 
									empleado36 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, funcion=funcion, estadoCivil=estadocivil,
									categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones,
									horarioSabadoInicio=horarioSabadoInicio, horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, 
									horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin)
									empleado36.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si trabaja en mas de un turno los domingos y feriados, pero no los sabados
									empleado37 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoFin=horarioSabadoFin, funcion=funcion, 
									horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, horarioFeriadoInicio=horarioFeriadoInicio, 
									horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin,
									estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado37.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='1':#si no trabaja en mas de un turno
									empleado38 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, funcion=funcion, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoFin=horarioSabadoFin, horarioFeriadoInicio=horarioFeriadoInicio, 
									horarioFeriadoFin=horarioFeriadoFin, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado38.save()
									return HttpResponseRedirect('/')	
								elif horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='0' and horarioAdicionalFeriado=='0':#si trabaja en mas de un turno
									empleado39 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoFin=horarioSabadoFin,  horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, 
									horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, horarioDomingoAdicionalInicio=horarioAdicionalDomingoInicio, horarioDomingoAdicionalFin=horarioAdicionalDomingoFin, horarioFeriadoInicio=horarioFeriadoInicio, 
									horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio,  horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin,
									funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado39.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalSabado=='1' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si trabaja en mas de un turno los feriados, pero no los sabados y domingos 
									empleado40 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, funcion=funcion, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoFin=horarioSabadoFin, horarioFeriadoInicio=horarioFeriadoInicio, 
									horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, 
									horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado40.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalSabado=='0' and horarioAdicionalDomingo=='1' and horarioAdicionalFeriado=='0':#si trabaja en mas de un turno los domingos, pero no los sabados y feriados
									empleado41 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, horarioDomingoFin=horarioDomingoFin,
									horarioDomingoInicio=horarioDomingoInicio, horarioSabadoInicio=horarioSabadoInicio, horarioSabadoFin=horarioSabadoFin, horarioSabadoAdicionalInicio=horarioAdicionalSabadoInicio, 
									horarioSabadoAdicionalFin=horarioAdicionalSabadoFin, horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, 
									horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado41.save()
									return HttpResponseRedirect('/')	
			
							elif trabajaFinde=='3' and horarioFeriado=='0':#si no trabaja sabado y domingo, pero si los feriados
								if horarioAdicionalFeriado=='1':#si trabaja los feriados en un solo turno
									empleado42 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, 
									horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, 
									fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado42.save()
									return HttpResponseRedirect('/')
								elif horarioAdicionalFeriado=='0':#si trabaja los feriados en mas de un turno
									empleado43 = Empleado.objects.create(consorcio_id=con.id, nombre=nombre, apellido=apellido, dni=dni, cuil=cuil, email=email, nacionalidad=nacionalidad, 
									telFijo=telFijo, celular=celular, direccion=direccion, localidad=localidad, cp=cp, estudios=estudios, ingreso=fechaIngreso, 
									horarioFeriadoInicio=horarioFeriadoInicio, horarioFeriadoFin=horarioFeriadoFin, horarioFeriadoAdicionalInicio=horarioAdicionalFeriadoInicio, 
									horarioFeriadoAdicionalFin=horarioAdicionalFeriadoFin, funcion=funcion, estadoCivil=estadocivil, categoriaFuncion=categoria, fechaNacimiento=fechaNacimiento, observaciones=observaciones)
									empleado43.save()
									return HttpResponseRedirect('/')	
					else:
						context = {}
						return render(request, "agregarConsorcio.html", context)
		else:
			context = {}
			return render(request, "agregarEmpleado.html", context)	
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
	
#----------------------------------------------------------------RECLAMOS-----------------------------------------------------------------------------
		
def mostrarReclamo(request):	#Funcion para mostrar los reclamos en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			consorcio = request.POST['consorcio']
			resultado = 0
			if resultado==0:
				consorcios = Consorcio.objects.filter(id = consorcio) #Verifico si el consorcio existe para modificarlo
				if consorcios.exists() == True: #CONSORCIO EXISTENTE
					validacionConsorcio = Consorcio
					con = Consorcio.objects.get(id=consorcio)
					reclamos = Reclamo.objects.all().filter(consorcio_id=con.id, esBaja=0)
					page = request.GET.get('page', 1)
					listaconsorcios = Consorcio.objects.all()
					listauf = UnidadFuncional.objects.all()
					
					
					page = request.GET.get('page', 1)
					
					paginator = Paginator(reclamos, page)
					
					try:
						reclamo = paginator.page(page)
					except PageNotAnInteger:
						reclamo = paginator.page(20)
					except EmptyPage:
						reclamo = paginator.page(paginator.num_pages)
					return render_to_response('reclamo.html', {'reclamo':reclamo,'reclamos':reclamos,'listaconsorcios':listaconsorcios,'listauf':listauf}, context_instance=RequestContext(request))
				
				else:
					context = {}
					return render(request, "mostrarReclamoError.html", context)	
		else:
			return render_to_response('mostrarReclamo.html', context_instance=RequestContext(request))
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')

def agregarReclamo(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":

			resultado = 1

			fecha = request.POST['fecha']
			ubicacion = request.POST['ubicacion']
			piso = request.POST['piso'] # ES LA UNIDAD FUNCIONAL!
			consorcio = request.POST['consorcio']
			estado = request.POST['estado']
			observaciones = request.POST['observaciones']
			if ubicacion == 'Particular':
				numero = request.POST['numero']
				estaAlquilado = request.POST['estaAlquilado']

					# Propietario
				nombre = request.POST['nombre']
				apellido = request.POST['apellido']
				dni = request.POST['dni']
				email = request.POST['email']
				telFijo = request.POST['telFijo']
				celular = request.POST['celular']
				localidad = request.POST['localidad']
				cp = request.POST['cp']
				direccion = request.POST['direccion']

					# Inquilino
				nombres = request.POST['nombres']
				apellidos = request.POST['apellidos']
				dnis = request.POST['dnis']
				emails = request.POST['emails']
				telFijos = request.POST['telFijos']
				celulars = request.POST['celulars']
			resultado = 0

			if resultado == 0:

				consorcios = Consorcio.objects.filter(id=consorcio)  # Verifico si el consorcio existe,
				if consorcios.exists() == True:
					con = Consorcio.objects.get(id=consorcio)  # Traigo el consorcio por id para asociarselo al reclamo
					
					# SI EL RECLAMO ES EN PARTES COMUNES
					if ubicacion == 'Comun':
						reclamo = Reclamo.objects.create(fecha=fecha, ubicacion='Comun',consorcio_id=con.id, estado=estado,descripcion=observaciones)
						reclamo.save()
						return render_to_response('accionExitosa.html', context_instance=RequestContext(request))
					
					else:
						dptoVerificacion = UnidadFuncional.objects.filter(unidadFuncional=piso, consorcio_id =con.id)
						if dptoVerificacion.exists() == True:
							uf = UnidadFuncional.objects.get(unidadFuncional=piso, consorcio_id =con.id)  # Traigo la UnidadFuncional por UF  para asociarselo al reclamo
							propietario = Propietario.objects.get(id=uf.propietario_id)
							propietario.nombre = nombre
							propietario.apellido = apellido 
							propietario.dni = dni
							propietario.email = email
							propietario.telFijo = telFijo
							propietario.celular = celular
							propietario.localidad = localidad
							propietario.cp = cp
							propietario.direccion = direccion
							propietario.save()
							if estaAlquilado == '0':
								inquilino = Inquilino.objects.create(nombre=nombres, apellido=apellidos, dni=dnis,email=emails, telFijo=telFijos, celular=celulars)
								inquilino.save()
								#Traigo el inquilino con los datos que lo cree para obtener su ID
							
								reclamo = Reclamo.objects.create(fecha=fecha, ubicacion=ubicacion, unidadFuncional_id=uf.id, consorcio_id=con.id,  estado=estado, descripcion=observaciones)
								reclamo.save()
								return render_to_response('accionExitosa.html', context_instance=RequestContext(request))
							else:
								reclamo = Reclamo.objects.create(fecha=fecha, ubicacion=ubicacion, unidadFuncional_id=uf.id, consorcio_id=con.id,  estado=estado, descripcion=observaciones)
								reclamo.save()
								return render_to_response('accionExitosa.html', context_instance=RequestContext(request))

						else: # SI NO EXISTE LA UF EN EL CONSORCIO, LO CREO

							if estaAlquilado == '0':
								propietario = Propietario.objects.create(nombre = nombre,apellido = apellido,dni = dni,email = email,telFijo = telFijo, celular = celular,localidad = localidad,cp = cp,direccion = direccion)
								propietario.save()
								inquilino = Inquilino.objects.create(nombre=nombres, apellido=apellidos, dni=dnis,email=emails, telFijo=telFijos, celular=celulars)
								inquilino.save()
								unidadFuncional = UnidadFuncional.objects.create(consorcio_id = con.id, propietario_id = propietario.id, inquilino_id= inquilino.id, alquilado = 1, unidadFuncional = piso, pisoDepartamento= numero)
								unidadFuncional.save()
								reclamo = Reclamo.objects.create(fecha=fecha, ubicacion=ubicacion, unidadFuncional_id=unidadFuncional.id,  consorcio_id=con.id,  estado=estado, descripcion=observaciones)
								reclamo.save()
								return render_to_response('accionExitosa.html', context_instance=RequestContext(request))
							else:
								propietario = Propietario.objects.create(nombre = nombre,apellido = apellido,dni = dni,email = email,telFijo = telFijo, celular = celular,localidad = localidad,cp = cp,direccion = direccion)
								unidadFuncional = UnidadFuncional.objects.create(consorcio_id = con.id, propietario_id = propietario.id,  alquilado = 0, unidadFuncional = piso, pisoDepartamento= numero)
								unidadFuncional.save()
								propietario.save()
								reclamo = Reclamo.objects.create(fecha=fecha, ubicacion=ubicacion, unidadFuncional_id=unidadFuncional.id,  consorcio_id=con.id,  estado=estado, descripcion=observaciones)
								reclamo.save()		
								return render_to_response('accionExitosa.html', context_instance=RequestContext(request))	
			
				else: # SI EL CONSORCIO NO EXISTE; ERROR
					context = {}
					return render(request, "agregarReclamo2.html", context)	
		else:
			context = {}
			return render(request, "agregarReclamo.html", context)	
	else:
		return redirect('/AdminConsorcios/usuario/iniciarsesion/')
					

def mostrarReclamoArchivado(request):	#Funcion para mostrar los reclamos en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			consorcio = request.POST['consorcio']
			resultado = 0
			if resultado==0:
				consorcios = Consorcio.objects.filter(id = consorcio) #Verifico si el consorcio existe para modificarlo
				if consorcios.exists() == True: #CONSORCIO EXISTENTE
					con = Consorcio.objects.get(id=consorcio)
					reclamos = Reclamo.objects.filter(consorcio_id=con.id, esBaja=1)
					listaconsorcios = Consorcio.objects.all()
					listauf = UnidadFuncional.objects.all()
					return render_to_response('mostrarReclamo1.html', {'reclamos':reclamos,'listaconsorcios':listaconsorcios,'listauf':listauf}, context_instance=RequestContext(request))
				else:
					context = {}
					return render(request, "mostrarReclamoError.html", context)	
		else:
			return render_to_response('mostrarReclamo.html', context_instance=RequestContext(request))
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')		

def archivarReclamo(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			id = request.POST['id']
			valor = request.POST['valor']
			resultado = 0
			if resultado==0:
				validacionReclamo = Reclamo.objects.filter(id=id)
				if validacionReclamo.exists() == True:
					reclamo = Reclamo.objects.get(id=id)
					if valor=='1':
						reclamo.esBaja = 1 #El reclamo es dado de baja (esBaja=true)
						reclamo.save()
						context = {}
						return render(request, "accionExitosa.html", context)	
					elif valor=='2':
						return HttpResponseRedirect('/AdminConsorcios/mostrarReclamo/')	
				else:
					context = {}
					return render(request, "archivarReclamoError.html", context)	
		else:
			context = {}
			return render(request, "archivarReclamo.html", context)			
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
		 
def modificarReclamo(request, id):	#
	if request.user.is_authenticated():#Si el usuario esta identificado
		reclamos = Reclamo.objects.get(id = id)
		
		if request.method == "GET":
			departamentoVerificacion = UnidadFuncional.objects.filter(unidadFuncional = reclamos.unidadFuncional_id)
			if departamentoVerificacion.exists() == True: #VERIFICO QUE EXISTA LA UF
				datos={'id':reclamos.id,'fecha':reclamos.fecha,'consorcio':reclamos.consorcio.id,'ubicacion':reclamos.ubicacion,
				'descripcion':reclamos.descripcion, 'estado':reclamos.estado, 'unidadFuncional':reclamos.unidadFuncional.unidadFuncional, 'piso':reclamos.unidadFuncional.pisoDepartamento}
				return render_to_response('modificarReclamo.html', datos, context_instance=RequestContext(request))
			else:
				datos={'id':reclamos.id,'fecha':reclamos.fecha,'consorcio':reclamos.consorcio.id,'ubicacion':reclamos.ubicacion,
				'descripcion':reclamos.descripcion, 'estado':reclamos.estado}
				return render_to_response('modificarReclamo.html', datos, context_instance=RequestContext(request))
					
		if request.method == "POST":
			resultado = 1
			ubicacion = request.POST['ubicacion']
			nroReclamo = request.POST['nroReclamo']
			estado = request.POST['estado']
			descripcion = request.POST['observaciones']
			fechas = request.POST['fechas']
			consorcios = request.POST['consorcios']
			if ubicacion == 'Particular':
				numero = request.POST['numero'] 
				piso = request.POST['piso']
			resultado = 0
			
			if resultado==0:
				
				consorcios1 = Consorcio.objects.filter(id = consorcios) #Verifico si el consorcio existe para modificarlo
				if consorcios1.exists() == True: #CONSORCIO EXISTENTE
					cons = Consorcio.objects.get(id = consorcios)
					reclamos.id = nroReclamo
					reclamos.ubicacion = ubicacion
					reclamos.estado = estado
					reclamos.fecha = fechas
					reclamos.consorcio_id = cons.id
					reclamos.descripcion = descripcion
							
					if ubicacion == 'Particular':
						dptoVerificacion = UnidadFuncional.objects.filter(consorcio_id = cons.id, unidadFuncional = numero)
						if dptoVerificacion.exists() == True: #VERIFICO QUE EXISTA LA UF
							dpto = UnidadFuncional.objects.get(unidadFuncional = numero, consorcio_id = cons.id)
							reclamos.unidadFuncional = dpto
							reclamos.save()
							context = {}
							return render(request, "accionExitosa.html", context)	
						else:
							context = {}
							return render(request, "ingresarUnidadFuncional.html", context)	
					else:
						reclamos.save()
						context = {}
						return render(request, "accionExitosa.html", context)	
				else:
					context = {}
					return render(request, "agregarConsorcio.html", context)			
		else:
			context = {}
			return render(request, "modificarReclamo.html", context)		
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
	
#----------------------------------------------------------------CAJA ADMINISTRACION-----------------------------------------------------------------------------	
	
def aperturaCajaAdministracion(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			tipo = request.POST['tipo']
			monto = request.POST['monto']
			moneda = request.POST['moneda']
			if tipo=='1':
				banco = request.POST['banco']
				cuenta = request.POST['cuenta']
			resultado = 0
			if resultado==0:
				admin = Administracion.objects.get(id=1);
				if not tipo=='1': #Si no es Bancaria
					verificacion = CajaAdministracion.objects.filter(tipoDeCaja = tipo)
					if verificacion.exists() == False:
						caja = CajaAdministracion.objects.create(administracion_id= admin.id, tipoDeCaja=tipo, montoActual=monto, moneda=moneda)
						caja.save()
						context = {}
						return render(request, "accionExitosa.html", context)	
					else:
						context = {}
						return render(request, "aperturaCA.html", context)
				if tipo=='1': #Si es Bancaria
					cajas = CajaAdministracion.objects.create(administracion_id= admin.id, tipoDeCaja=tipo, banco=banco, nroCuenta=cuenta, montoActual=monto, moneda=moneda)
					cajas.save()
					context = {}
					return render(request, "accionExitosa.html", context)	
		else:
			context = {}
			return render(request, "aperturaCA.html", context)
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')	

def eliminarCajaAdministracion(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			tipo = request.POST['tipo']
			valor = request.POST['valor']
			if tipo=='1':
				banco = request.POST['banco']
				cuenta = request.POST['cuenta']
			resultado = 0
			if resultado==0:
				if not tipo == '1': #Si no es Bancaria
					verificacionCaja = CajaAdministracion.objects.filter(tipoDeCaja=tipo)
					if verificacionCaja.exists() == False:	#Si no existe, ERROR
						context = {}
						return render(request, "eliminarCAError.html", context)
					else:
						caja = CajaAdministracion.objects.get(tipoDeCaja=tipo)
						if valor=='1':
							caja.delete()
							context = {}
							return render(request, "accionExitosa.html", context)	
						elif valor=='2':
							return HttpResponseRedirect('/')
						
				if tipo=='1': #Si es Bancaria
					verificacionCajaAdminBancaria = CajaAdministracion.objects.filter(tipoDeCaja=1, banco=banco, nroCuenta=cuenta)
					if verificacionCajaAdminBancaria.exists() == False:	#Si no existe, ERROR
						context = {}
						return render(request, "eliminarCAError.html", context)
					else:
						cajas = CajaAdministracion.objects.get(tipoDeCaja=tipo, banco=banco, nroCuenta=cuenta)
						if valor=='1':
							cajas.delete()
							context = {}
							return render(request, "accionExitosa.html", context)	
						elif valor=='2':
							return HttpResponseRedirect('/')		
		else:
			context = {}
			return render(request, "eliminarCA.html", context)				
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
		 
def mostrarCajaAdministracion(request):	#Funcion para mostrar las cajas de la Administracion en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado
		cajas = CajaAdministracion.objects.all()
		return render_to_response('cajaAdmin.html', {'cajas':cajas}, context_instance=RequestContext(request))
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
		
	
#----------------------------------------------------------------CAJA CONSORCIO-----------------------------------------------------------------------------	
	
def aperturaCajaConsorcio(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			consorcio = request.POST['consorcio']
			tipo = request.POST['tipo']
			monto = request.POST['monto']
			moneda = request.POST['moneda']
			if tipo=='1':#Si es Bancaria
				banco = request.POST['banco']
				cuenta = request.POST['cuenta']
			resultado = 0
			if resultado==0:
				consorcios = Consorcio.objects.filter(id = consorcio) #Verifico si el consorcio existe para modificarlo
				if consorcios.exists() == True: #CONSORCIO EXISTENTE
					con = Consorcio.objects.get(id = consorcio)
					if not tipo=='1': #Si no es Bancaria
						verificacion = CajaConsorcio.objects.filter(tipoDeCaja = tipo , consorcio_id = con.id)
						if verificacion.exists() == False: #SI LA CAJA del consorcio no existe
							caja = CajaConsorcio.objects.create(consorcio_id = con.id, tipoDeCaja = tipo, montoActual = monto, moneda=moneda)
							caja.save()
							context = {}
							return render(request, "accionExitosa.html", context)	
						else:
							context = {}
							return render(request, "aperturaCC3.html", context)
					if tipo=='1': #Si es Bancaria
						cajas = CajaConsorcio.objects.create(consorcio_id = con.id, tipoDeCaja=tipo, banco=banco, nroCuenta=cuenta, montoActual=monto, moneda=moneda)
						cajas.save()
						context = {}
						return render(request, "accionExitosa.html", context)	
				else:
					context = {}
					return render(request, "aperturaCC2.html", context)
		else:
			context = {}
			return render(request, "aperturaCC.html", context)
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')		

def eliminarCajaConsorcio(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			tipo = request.POST['tipo']
			consorcio = request.POST['consorcio']
			valor = request.POST['valor']
			if tipo=='1':#Si es Bancaria
				banco = request.POST['banco']
				cuenta = request.POST['cuenta']
			resultado = 0
			if resultado == 0:
			
				con = Consorcio.objects.get(id = consorcio)
				if not tipo == '1': #Si no es Bancaria
					verificacionCaja = CajaConsorcio.objects.filter(tipoDeCaja=tipo)
					if verificacionCaja.exists() == False:	#Si no existe, ERROR
						context = {}
						return render(request, "eliminarCCError.html", context)
					else:
						caja = CajaConsorcio.objects.get(tipoDeCaja=tipo, consorcio_id=con.id)
						if valor == '1': # Si estoy seguro, entonces lo borro.
							caja.delete()
							context = {}
							return render(request, "accionExitosa.html", context)	
						elif valor=='2':
							context = {}
							return render(request, "accionExitosa.html", context)	
						
				if tipo=='1': #Si es Bancaria
					verificacionCajaConsorcioBancaria = CajaConsorcio.objects.filter(tipoDeCaja=1, banco=banco, nroCuenta=cuenta)
					if verificacionCajaConsorcioBancaria.exists() == False:	#Si no existe, ERROR
						context = {}
						return render(request, "eliminarCCError.html", context)
					else:
						cajas = CajaConsorcio.objects.get(consorcio_id=con.id, tipoDeCaja=tipo, banco=banco, nroCuenta=cuenta)
						if valor=='1':
							cajas.delete()
							context = {}
							return render(request, "accionExitosa.html", context)	
						elif valor=='2':
							context = {}
							return render(request, "accionExitosa.html", context)	
		else:
			context = {}
			return render(request, "eliminarCC.html", context)				
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
		 
def mostrarCajaConsorcio(request):	#Funcion para mostrar las cajas de la Administracion en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			consorcio = request.POST['consorcio']
			resultado = 0
			if resultado==0:
				consorcios = Consorcio.objects.filter(id = consorcio) #Verifico si el consorcio existe para modificarlo
				if consorcios.exists() == True: #CONSORCIO EXISTENTE
					con = Consorcio.objects.get(id = consorcio)
					cajascon = CajaConsorcio.objects.filter(consorcio_id=con.id)
					return render_to_response('cajaConsorcio.html', {'cajascon':cajascon}, context_instance=RequestContext(request))
				else:
					return render_to_response('mostrarCC2.html', context_instance=RequestContext(request))
		else:
			return render_to_response('mostrarCC.html', context_instance=RequestContext(request))	
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
		
#----------------------------------------------------------------FACTURAS-----------------------------------------------------------------------------		
		
def archivarFactura(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			numero = request.POST['numero']
			valor = request.POST['valor']
			resultado = 0
			if resultado==0:
				verificacionFactura = Factura.objects.filter(numero=numero)#VALIDO QUE EXISTA LA FACTURA
				if verificacionFactura.exists() == True:
					factura = Factura.objects.get(numero=numero)
					if valor=='1':
						factura.esBaja = 1 #La factura es dada de baja (esBaja=true)
						factura.save()
						context = {}
						return render(request, "accionExitosa.html", context)	
					elif valor=='2':
						context = {}
						return render(request, "accionExitosa.html", context)	
				else:
					context = {}
					return render(request, "archivarFacturaError.html", context)	
		else:
			context = {}
			return render(request, "archivarFactura.html", context)	
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
		 
def mostrarFacturaArchivada(request):	#Funcion para mostrar las Facturas archivadas
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			valor = request.POST['valor']
			consorcio = request.POST['consorcio']
			resultado = 0
			if resultado==0:
				if valor=='1':
					admin = Administracion.objects.get(id = 1)
					cajasAdministracion = CajaAdministracion.objects.all()
					factura = Factura.objects.all().filter(esBaja = 1)
					
					#-------PARA TODAS LAS FACTURAS DE LA CAJA EFECTIVA
					facturasEfectivo = []
					verificacionCajaEfectiva = CajaAdministracion.objects.filter(administracion_id =admin.id, tipoDeCaja=3)
					if verificacionCajaEfectiva.exists() == True:	#Si no existe, la creo
						cajaAdministracionEfectiva = CajaAdministracion.objects.get(tipoDeCaja =3)
						
						for dato in factura:
							if dato.cajaAdministracion_id == cajaAdministracionEfectiva.id:
								facturasEfectivo.append(dato)
						facturasEfectivo.sort(key=lambda factura: factura.fechaPago,reverse=True)	
							
					#-------PARA TODAS LAS FACTURAS DE LA CAJA CHEQUE
					facturasCheque = []
					verificacionCajaCheque = CajaAdministracion.objects.filter(administracion_id =admin.id, tipoDeCaja=2)
					if verificacionCajaCheque.exists() == True:
						cajaAdministracionCheque = CajaAdministracion.objects.get(tipoDeCaja =2)
						
						for dato in factura:
							if dato.cajaAdministracion_id == cajaAdministracionCheque.id:
								facturasCheque.append(dato)
						facturasCheque.sort(key=lambda factura: factura.fechaPago,reverse=True)	
					
					#-------PARA TODAS LAS FACTURAS DE LA CAJA OTRAS
					facturasOtras = []
					verificacionCajaOtras = CajaAdministracion.objects.filter(administracion_id =admin.id, tipoDeCaja=4)
					if verificacionCajaOtras.exists() == True:	
						cajaAdministracionOtras = CajaAdministracion.objects.get(tipoDeCaja =4)
						for dato in factura:
							if dato.cajaAdministracion_id == cajaAdministracionOtras.id:
								facturasOtras.append(dato)
						facturasOtras.sort(key=lambda factura: factura.fechaPago,reverse=True)	
					
					#-------PARA TODAS LAS FACTURAS DE LA CAJA VALES
					facturasVales = []
					verificacionCajaVales = CajaAdministracion.objects.filter(administracion_id =admin.id, tipoDeCaja=5)
					if verificacionCajaVales.exists() == True:	
						cajaAdministracionVales = CajaAdministracion.objects.get(tipoDeCaja =5)
						for dato in factura:
							if dato.cajaAdministracion_id == cajaAdministracionVales.id:
								facturasVales.append(dato)
						facturasVales.sort(key=lambda factura: factura.fechaPago,reverse=True)	
					
					#-------PARA TODAS LAS FACTURAS DE LA CAJA BANCARIA
					facturasBanco = []
					verificacionCajaAdminBancaria = CajaAdministracion.objects.filter(administracion_id =admin.id, tipoDeCaja=1)
					if verificacionCajaAdminBancaria.exists() == True:	
						CajaAdministracionBancos = CajaAdministracion.objects.all().filter(tipoDeCaja=1)
						for dato in CajaAdministracionBancos:
							for dato1 in factura:
								if dato.id == dato1.cajaAdministracion_id:
									facturasBanco.append(dato1)
						facturasBanco.sort(key=lambda factura: factura.fechaPago,reverse=True)	
					
					#-------PARA TODAS LAS FACTURAS DE LA ADMINISTRACION
					facturasAdministracion = []
					for dato in cajasAdministracion:
						for dato1 in factura:
							if dato.id == dato1.cajaAdministracion_id:
								facturasAdministracion.append(dato1)
					facturasAdministracion.sort(key=lambda factura: factura.fechaPago,reverse=True)	
					
					return render_to_response('mostrarFacturasArchivadasAdministracion.html', {'facturasEfectivo':facturasEfectivo, 'facturasCheque':facturasCheque,
					'facturasOtras':facturasOtras, 'facturasVales': facturasVales, 'facturasBanco':facturasBanco,
					'cajaAdmin': cajasAdministracion, 'facturasAdministracion':facturasAdministracion}, context_instance=RequestContext(request))
				
				
				elif valor=='2':#---------------- Para facturas del CONSORCIO---------------------
					verificacionConsorcio = Consorcio.objects.filter(id=consorcio)
					if verificacionConsorcio.exists() == True:
						con = Consorcio.objects.get(id = consorcio)
						cajasConsorcios = CajaConsorcio.objects.all().filter(consorcio_id = con.id)
						facturasConsorcio = Factura.objects.all().filter(esBaja = 1)
						
						#-------PARA TODAS LAS FACTURAS DE LA CAJA EFECTIVA
						facturasConsorcioEfectivo = []
						verificacionCajaConsorcioEfectiva = CajaConsorcio.objects.filter(consorcio_id =con.id, tipoDeCaja=3)
						if verificacionCajaConsorcioEfectiva.exists() == True:	#Si no existe la caja del consorcio, la creo
							cajaConsorcioEfectiva = CajaConsorcio.objects.all().filter(tipoDeCaja = 3, consorcio_id = con.id)
							for dato in facturasConsorcio:
								for dato1 in cajaConsorcioEfectiva:
									if dato.cajaConsorcio_id == dato1.id:
										facturasConsorcioEfectivo.append(dato)
							facturasConsorcioEfectivo.sort(key=lambda factura: factura.fechaPago,reverse=True)
						
						#-------PARA TODAS LAS FACTURAS DE LA CAJA CHEQUE
						facturasConsorcioCheque = []
						verificacionCajaConsorcioCheque = CajaConsorcio.objects.filter(consorcio_id =con.id, tipoDeCaja=2)
						if verificacionCajaConsorcioCheque.exists() == True:	#Si no existe la caja del consorcio, la creo
							cajaConsorcioCheque = CajaConsorcio.objects.all().filter(tipoDeCaja =2, consorcio_id = con.id)
							for dato in facturasConsorcio:
								for dato1 in cajaConsorcioCheque:
									if dato.cajaConsorcio_id == dato1.id:
										facturasConsorcioCheque.append(dato)
							facturasConsorcioCheque.sort(key=lambda factura: factura.fechaPago,reverse=True)
						
						#-------PARA TODAS LAS FACTURAS DE LA CAJA BANCARIA
						facturasConsorcioBancos = []
						verificacionCajaConsorcioBancaria = CajaConsorcio.objects.filter(consorcio_id =con.id, tipoDeCaja=1)
						if verificacionCajaConsorcioBancaria.exists() == True:	#Si no existe la caja del consorcio, la creo
							CajaConsorcioBancos = CajaConsorcio.objects.all().filter(tipoDeCaja=1)
							for dato in CajaConsorcioBancos:
								for dato1 in facturasConsorcio:
									if dato.id == dato1.cajaConsorcio_id:
										facturasConsorcioBancos.append(dato1)
							facturasConsorcioBancos.sort(key=lambda factura: factura.fechaPago,reverse=True)
						
						#-------PARA TODAS LOS PAGO DE EXPENSAS-------------------
						facturasConsorcioExpensas = []
						
						for dato in facturasConsorcio:
							for dato1 in cajasConsorcios:
								if dato.factura == 'Pago de Expensas' and dato.cajaConsorcio_id == dato1.id:
									facturasConsorcioExpensas.append(dato)
						facturasConsorcioExpensas.sort(key=lambda factura: factura.fechaPago,reverse=True)			
									
						#-------PARA TODAS LAS FACTURAS DEL CONSORCIO
						facturasConsorcioT = []
						for dato in cajasConsorcios:
							for dato1 in facturasConsorcio:
								if dato.id == dato1.cajaConsorcio_id:
									facturasConsorcioT.append(dato1)
						facturasConsorcioT.sort(key=lambda factura: factura.fechaPago,reverse=True)	
								
						return render_to_response('mostrarFacturasArchivadasConsorcio.html', {'consorcio':consorcio,'facturasConsorcioEfectivo':facturasConsorcioEfectivo,
						'cajaConsorcios': cajasConsorcios,'facturasConsorcioBancos':facturasConsorcioBancos,
						'facturasConsorcioT':facturasConsorcioT,
						'facturasConsorcioCheque':facturasConsorcioCheque,'facturasConsorcioExpensas':facturasConsorcioExpensas}, context_instance=RequestContext(request))
					else:
						return render_to_response('mostrarFacturaArchivadaError.html', context_instance=RequestContext(request))
		
		else:		
			return render_to_response('mostrarFactura.html', context_instance=RequestContext(request))
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')			
			
def mostrarFactura(request):	#Funcion para mostrar los consorcios en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			valor = request.POST['valor']
			consorcio = request.POST['consorcio']
			resultado = 0
			if resultado==0:
				if valor=='1':
					admin = Administracion.objects.get(id = 1)
					cajasAdministracion = CajaAdministracion.objects.all()
					
					#-------PARA TODAS LAS FACTURAS DE LA CAJA EFECTIVA
					facturasEfectivo = []
					verificacionCajaEfectiva = CajaAdministracion.objects.filter(administracion_id =admin.id, tipoDeCaja=3)
					if verificacionCajaEfectiva.exists() == True:	#Si no existe, la creo
						cajaAdministracionEfectiva = CajaAdministracion.objects.get(tipoDeCaja =3)
						factura = Factura.objects.all()
						for dato in factura:
							if dato.cajaAdministracion_id == cajaAdministracionEfectiva.id:
								facturasEfectivo.append(dato)
						facturasEfectivo.sort(key=lambda factura: factura.fechaPago,reverse=True)	
							
					#-------PARA TODAS LAS FACTURAS DE LA CAJA CHEQUE
					facturasCheque = []
					verificacionCajaCheque = CajaAdministracion.objects.filter(administracion_id =admin.id, tipoDeCaja=2)
					if verificacionCajaCheque.exists() == True:
						cajaAdministracionCheque = CajaAdministracion.objects.get(tipoDeCaja =2)
						
						for dato in factura:
							if dato.cajaAdministracion_id == cajaAdministracionCheque.id:
								facturasCheque.append(dato)
						facturasCheque.sort(key=lambda factura: factura.fechaPago,reverse=True)	
					
					#-------PARA TODAS LAS FACTURAS DE LA CAJA OTRAS
					facturasOtras = []
					verificacionCajaOtras = CajaAdministracion.objects.filter(administracion_id =admin.id, tipoDeCaja=4)
					if verificacionCajaOtras.exists() == True:	
						cajaAdministracionOtras = CajaAdministracion.objects.get(tipoDeCaja =4)
						for dato in factura:
							if dato.cajaAdministracion_id == cajaAdministracionOtras.id:
								facturasOtras.append(dato)
						facturasOtras.sort(key=lambda factura: factura.fechaPago,reverse=True)	
					
					#-------PARA TODAS LAS FACTURAS DE LA CAJA VALES
					facturasVales = []
					verificacionCajaVales = CajaAdministracion.objects.filter(administracion_id =admin.id, tipoDeCaja=5)
					if verificacionCajaVales.exists() == True:	
						cajaAdministracionVales = CajaAdministracion.objects.get(tipoDeCaja =5)
						for dato in factura:
							if dato.cajaAdministracion_id == cajaAdministracionVales.id:
								facturasVales.append(dato)
						facturasVales.sort(key=lambda factura: factura.fechaPago,reverse=True)	
					
					#-------PARA TODAS LAS FACTURAS DE LA CAJA BANCARIA
					facturasBanco = []
					verificacionCajaAdminBancaria = CajaAdministracion.objects.filter(administracion_id =admin.id, tipoDeCaja=1)
					if verificacionCajaAdminBancaria.exists() == True:	
						CajaAdministracionBancos = CajaAdministracion.objects.all().filter(tipoDeCaja=1)
						for dato in CajaAdministracionBancos:
							for dato1 in factura:
								if dato.id == dato1.cajaAdministracion_id:
									facturasBanco.append(dato1)
						facturasBanco.sort(key=lambda factura: factura.fechaPago,reverse=True)	
					
					#-------PARA TODAS LAS FACTURAS DE LA ADMINISTRACION
					facturasAdministracion = []
					for dato in cajasAdministracion:
						for dato1 in factura:
							if dato.id == dato1.cajaAdministracion_id:
								facturasAdministracion.append(dato1)
					facturasAdministracion.sort(key=lambda factura: factura.fechaPago,reverse=True)	
					
					return render_to_response('factura.html', {'facturasEfectivo':facturasEfectivo, 'facturasCheque':facturasCheque,
					'facturasOtras':facturasOtras, 'facturasVales': facturasVales, 'facturasBanco':facturasBanco,
					'cajaAdmin': cajasAdministracion, 'facturasAdministracion':facturasAdministracion}, context_instance=RequestContext(request))
				
				
				elif valor=='2':#---------------- Para facturas del CONSORCIO---------------------
					verificacionConsorcio = Consorcio.objects.filter(id=consorcio)
					if verificacionConsorcio.exists() == True:
						con = Consorcio.objects.get(id = consorcio)
						cajasConsorcios = CajaConsorcio.objects.all().filter(consorcio_id = con.id)
						facturasConsorcio = Factura.objects.all()
						
						#-------PARA TODAS LAS FACTURAS DE LA CAJA EFECTIVA
						facturasConsorcioEfectivo = []
						verificacionCajaConsorcioEfectiva = CajaConsorcio.objects.filter(consorcio_id =con.id, tipoDeCaja=3)
						if verificacionCajaConsorcioEfectiva.exists() == True:	#Si no existe la caja del consorcio, la creo
							cajaConsorcioEfectiva = CajaConsorcio.objects.all().filter(tipoDeCaja = 3, consorcio_id = con.id)
							for dato in facturasConsorcio:
								for dato1 in cajaConsorcioEfectiva:
									if dato.cajaConsorcio_id == dato1.id:
										facturasConsorcioEfectivo.append(dato)
							facturasConsorcioEfectivo.sort(key=lambda factura: factura.fechaPago,reverse=True)
						
						#-------PARA TODAS LAS FACTURAS DE LA CAJA CHEQUE
						facturasConsorcioCheque = []
						verificacionCajaConsorcioCheque = CajaConsorcio.objects.filter(consorcio_id =con.id, tipoDeCaja=2)
						if verificacionCajaConsorcioCheque.exists() == True:	#Si no existe la caja del consorcio, la creo
							cajaConsorcioCheque = CajaConsorcio.objects.all().filter(tipoDeCaja =2, consorcio_id = con.id)
							for dato in facturasConsorcio:
								for dato1 in cajaConsorcioCheque:
									if dato.cajaConsorcio_id == dato1.id:
										facturasConsorcioCheque.append(dato)
							facturasConsorcioCheque.sort(key=lambda factura: factura.fechaPago,reverse=True)
						
						#-------PARA TODAS LAS FACTURAS DE LA CAJA BANCARIA
						facturasConsorcioBancos = []
						verificacionCajaConsorcioBancaria = CajaConsorcio.objects.filter(consorcio_id =con.id, tipoDeCaja=1)
						if verificacionCajaConsorcioBancaria.exists() == True:	#Si no existe la caja del consorcio, la creo
							CajaConsorcioBancos = CajaConsorcio.objects.all().filter(tipoDeCaja=1)
							for dato in CajaConsorcioBancos:
								for dato1 in facturasConsorcio:
									if dato.id == dato1.cajaConsorcio_id:
										facturasConsorcioBancos.append(dato1)
							facturasConsorcioBancos.sort(key=lambda factura: factura.fechaPago,reverse=True)
						
						#-------PARA TODAS LOS PAGO DE EXPENSAS-------------------
						facturasConsorcioExpensas = []
						
						for dato in facturasConsorcio:
							for dato1 in cajasConsorcios:
								if dato.factura == 'Pago de Expensas' and dato.cajaConsorcio_id == dato1.id:
									facturasConsorcioExpensas.append(dato)
						facturasConsorcioExpensas.sort(key=lambda factura: factura.fechaPago,reverse=True)			
									
						#-------PARA TODAS LAS FACTURAS DEL CONSORCIO
						facturasConsorcioT = []
						for dato in cajasConsorcios:
							for dato1 in facturasConsorcio:
								if dato.id == dato1.cajaConsorcio_id:
									facturasConsorcioT.append(dato1)
						facturasConsorcioT.sort(key=lambda factura: factura.fechaPago,reverse=True)	
								
						return render_to_response('facturas.html', {'consorcio':consorcio,'facturasConsorcioEfectivo':facturasConsorcioEfectivo,
						'cajaConsorcios': cajasConsorcios,'facturasConsorcioBancos':facturasConsorcioBancos,
						'facturasConsorcioT':facturasConsorcioT,
						'facturasConsorcioCheque':facturasConsorcioCheque,'facturasConsorcioExpensas':facturasConsorcioExpensas}, context_instance=RequestContext(request))
					else:
						return render_to_response('mostrarFacturaErrorConsorcio.html', context_instance=RequestContext(request))
		else:		
			return render_to_response('mostrarFactura.html', context_instance=RequestContext(request))	
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
		 


def facturas(request):	#Funcion para mostrar los consorcios en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado
		return render_to_response('facturas.html', context_instance=RequestContext(request))
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')

def agregarFactura(request):	#Funcion para agregar las facturas en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado

		if request.method == "POST":
			resultado = 1
			seguir = request.POST['seguir']
			dato = request.POST['dato'] #Movimiento o pago de expensas
			pago = request.POST['pago']
			consorcio = request.POST['consorcio']
			observaciones = request.POST['observaciones']
			monto = request.POST['monto']
			
			#-------------------------EXPENSAS-------------------
			if dato =='Pago de Expensas':
				
				unidadfuncional = request.POST['unidadfuncional'] 
				depto = request.POST['depto']
				tipoCajaConsorcio = request.POST['tipoCajaConsorcio']
				caja = 2 #En el caso del pago de expensas la caja siempre es la del consorcio, por eso es siempre 2. Se lo setea porque no se la elige en la vista.
				if tipoCajaConsorcio == '1':
					banco = request.POST['banco']
					cuenta = request.POST['cuenta']
					
			#-------------------------MOVIMIENTOS-------------------		
			elif dato=='Movimiento':
				tipo = request.POST['tipo']
				emision =  request.POST['emision']
				caja = request.POST['caja']
				tipofactura = request.POST['tipofactura']
				nro = request.POST['nro']
				
				if caja == '1':
					tipoCaja = request.POST['tipoCaja']
					if tipoCaja == '1':
						banco = request.POST['banco']
						cuenta = request.POST['cuenta']	
				elif caja == '2':			
					tipoCajaConsorcio = request.POST['tipoCajaConsorcio']
					if tipoCajaConsorcio == '1':
						banco = request.POST['banco']
						cuenta = request.POST['cuenta']	
						
			resultado = 0
			
			if resultado==0:
				if caja=='1': #CAJA ADMINISTRACION
					admin = Administracion.objects.get(id=1)
					
					if tipoCaja=='1': #Si es Bancaria
						verificacionCajaAdminBancaria = CajaAdministracion.objects.filter(administracion_id =admin.id, tipoDeCaja=tipoCaja, banco=banco, nroCuenta=cuenta)
						if verificacionCajaAdminBancaria.exists() == False:	#Si no existe, la creo
							context = {}
							return render(request, "agregarFacturasErrorCajaAdministracion.html", context)
						else: #Si Existe la caja, prosigo	
							if dato=='Movimiento':#La factura es de servicios o gastos de la admin y/o consorcios
								cajaAdmin = CajaAdministracion.objects.get(administracion_id =admin.id, tipoDeCaja=tipoCaja, banco=banco, nroCuenta=cuenta)
								verificacionFacturaAdminBancaria = Factura.objects.filter(numero=nro)#VALIDO QUE NO HAYA OTRA FACTURA CON EL MISMO NUMERO
								if verificacionFacturaAdminBancaria.exists() == False:
									fact = Factura.objects.create(numero=nro, tipoDeFactura=tipofactura, factura=dato, fechaPago=pago, fechaEmision=emision, tipo=tipo, monto=monto, cajaAdministracion_id=cajaAdmin.id, observaciones=observaciones)	
									#En la Administracion el id=1 porque solo hay una Administracion
									fact.save()
									#Procedo a realizar los movimientos en las cajas 
									if fact.tipo == 'Ingreso' :
										cajaAdmin.montoActual = cajaAdmin.montoActual + float(fact.monto)
										cajaAdmin.save()
									else:
										cajaAdmin.montoActual = cajaAdmin.montoActual - float(fact.monto)
										cajaAdmin.save()
										if seguir=='si': 
											context = {} 
											return render(request, "agregarFacturas.html", context)	 
										else:	
											context = {}
											return render(request, "accionExitosa.html", context)		
								else:#SI EXISTE LA FACTURA; ERROR
									context = {}
									return render(request, "agregarFacturasErrorFactura.html", context)	
					elif not tipoCaja=='1': #Si no es Bancaria
						verificacionCajaAdmin = CajaAdministracion.objects.filter(administracion_id =admin.id, tipoDeCaja=tipoCaja)
						if verificacionCajaAdmin.exists() == False:	#Si no existe, la creo
							context = {}
							return render(request, "agregarFacturasErrorCajaAdministracion.html", context)
						else:
							if dato=='Movimiento':#La factura es de servicios o gastos de la admin y/o consorcios
								cajaAdminN = CajaAdministracion.objects.get(administracion_id =admin.id, tipoDeCaja=tipoCaja)
								verificacionFacturaAdmin = Factura.objects.filter(numero=nro)#VALIDO QUE NO HAYA OTRA FACTURA CON EL MISMO NUMERO
								if verificacionFacturaAdmin.exists() == False:
									fact = Factura.objects.create(numero=nro, factura=dato, tipoDeFactura=tipofactura, fechaEmision=emision, fechaPago=pago, tipo=tipo, monto=monto, cajaAdministracion_id=cajaAdminN.id, observaciones=observaciones)	
									#En la Administracion el id=1 porque solo hay una Administracion
									fact.save()
									#Procedo a realizar los movimientos en las cajas 
									if fact.tipo == 'Ingreso' :
										cajaAdminN.montoActual = cajaAdminN.montoActual + float(fact.monto)
										cajaAdminN.save()
									else:
										cajaAdminN.montoActual = cajaAdminN.montoActual - float(fact.monto)
										cajaAdminN.save()
									if seguir=='si': 
										context = {} 
										return render(request, "agregarFacturas.html", context)	 
									else:	
										context = {}
										return render(request, "accionExitosa.html", context)	
								else:#SI EXISTE LA FACTURA; ERROR
									context = {}
									return render(request, "agregarFacturasErrorFactura.html", context)	
				else: #Si es caja 2 CONSORCIOS
					verificacionConsorcio = Consorcio.objects.filter(id=consorcio)
					if verificacionConsorcio.exists() == False:	#Si no existe el consorcio, lo creo
						context = {}
						return render(request, "agregarFacturasErrorConsorcio.html", context)
					else: #Si existe el consorcio, prosigo
						con = Consorcio.objects.get(id=consorcio) #Traigo el consorcio por el id para poder asociar la caja de ese consorcio
						if tipoCajaConsorcio=='1': #Si es Bancaria
							verificacionCajaConsorcioBancaria = CajaConsorcio.objects.filter(consorcio_id =con.id, tipoDeCaja=tipoCajaConsorcio, banco=banco, nroCuenta=cuenta)
							if verificacionCajaConsorcioBancaria.exists() == False:	#Si no existe, la creo
								context = {}
								return render(request, "agregarFacturasErrorCajaAdministracion.html", context)
							else: #Si Existe la caja del consorcio, prosigo	
								cajacon = CajaConsorcio.objects.get(consorcio_id =con.id, tipoDeCaja=tipoCajaConsorcio, banco=banco, nroCuenta=cuenta)
								if dato == 'Movimiento':#La factura es de servicios o gastos de la admin y/o consorcios
									verificacionFacturaConsorcioBancaria = Factura.objects.filter(numero=nro)#VALIDO QUE NO HAYA OTRA FACTURA CON EL MISMO NUMERO
									if verificacionFacturaConsorcioBancaria.exists() == False:
										f = Factura.objects.create(numero=nro, tipoDeFactura=tipofactura, factura=dato, fechaPago=pago, fechaEmision=emision, tipo=tipo, monto=monto, observaciones=observaciones, cajaConsorcio_id=cajacon.id)	
										f.save()
										#Procedo a realizar los movimientos en las cajas 
										if f.tipo == 'Ingreso' :
											cajacon.montoActual = cajacon.montoActual + float(f.monto)
											cajacon.save()
										else:
											cajacon.montoActual = cajacon.montoActual - float(f.monto)
											cajacon.save()
										if seguir=='si': 
											context = {} 
											return render(request, "agregarFacturas.html", context)	 
										else:	
											context = {}
											return render(request, "accionExitosa.html", context)		
									else:#SI EXISTE LA FACTURA; ERROR
										context = {}
										return render(request, "agregarFacturasErrorFactura.html", context)		
								else:#Pago de Expensas 
									x = datetime.datetime.now()
									numeroCrearBancario ='E'+str(unidadfuncional)+str(x.month)+str(x.year-2000)+str(x.hour)+str(x.minute)+str(x.second)
									verificacionFacturaConsorcioBancariaExpensa = Factura.objects.filter(numero=factu.numero)#VALIDO QUE NO HAYA OTRA FACTURA CON EL MISMO NUMERO
									if verificacionFacturaConsorcioBancariaExpensa.exists() == False:
										factu = Factura.objects.create(numero =numeroCrearBancario ,cajaConsorcio_id=cajacon.id, unidadFuncional=unidadfuncional, pisoDepartamento=depto,factura=dato, fechaPago=pago, monto=monto, tipo= 'Ingreso',tipoDeFactura= 'E',  observaciones=observaciones)	
										factu.save()
										#Procedo a realizar los movimientos en las cajas
										cajacon.montoActual = cajacon.montoActual + float(factu.monto)
										cajacon.save()
										if seguir=='si': 
											context = {} 
											return render(request, "agregarFacturas.html", context)	 
										else:	
											context = {}
											return render(request, "accionExitosa.html", context)		
									else:#SI EXISTE LA Expensa; ERROR
										context = {}
										return render(request, "agregarFacturasErrorFactura.html", context)		
						else: #Si no es Bancaria
							verificacionCajaConsorcio = CajaConsorcio.objects.filter(consorcio_id =con.id, tipoDeCaja=tipoCajaConsorcio)
							if verificacionCajaConsorcio.exists() == False:	#Si no existe la caja del consorcio, la creo
								context = {}
								return render(request, "agregarFacturasErrorCajaAdministracion.html", context)
							else:#Si existe la caja del consorcio, prosigo
								cajacons = CajaConsorcio.objects.get(consorcio_id =con.id, tipoDeCaja=tipoCajaConsorcio)
								if dato=='Movimiento':#La factura es de servicios o gastos de la admin y/o consorcios
									verificacionFacturaConsorcio = Factura.objects.filter(numero=nro)#VALIDO QUE NO HAYA OTRA FACTURA CON EL MISMO NUMERO
									if verificacionFacturaConsorcio.exists() == False:
										f = Factura.objects.create(tipoDeFactura=tipofactura, factura=dato, numero=nro, fechaEmision=emision, fechaPago=pago, tipo=tipo, monto=monto, observaciones=observaciones, cajaConsorcio_id=cajacons.id)	
										f.save()
										#Procedo a realizar los movimientos en las cajas 
										if f.tipo == 'Ingreso' :
											cajacons.montoActual = cajacons.montoActual + float(f.monto)
											cajacons.save()
										else:
											cajacons.montoActual = cajacons.montoActual - float(f.monto)
											cajacons.save()
										if seguir=='si': 
											context = {} 
											return render(request, "agregarFacturas.html", context)	 
										else:	
											context = {}
											return render(request, "accionExitosa.html", context)			
								else:#Pago de Expensas 
									#for i in range(1, 20):
									x = datetime.datetime.now()
									numeroCrear ='E'+str(unidadfuncional)+str(x.month)+str(x.year-2000)+str(x.hour)+str(x.minute)+str(x.second) 
									verificacionFacturaConsorcioExpensa = Factura.objects.filter(numero=numeroCrear)#VALIDO QUE NO HAYA OTRA FACTURA CON EL MISMO NUMERO
									if verificacionFacturaConsorcioExpensa.exists() == False:
										facturaExpensa = Factura.objects.create(numero = numeroCrear, cajaConsorcio_id=cajacons.id, unidadFuncional=unidadfuncional, pisoDepartamento=depto,factura=dato, fechaPago=pago, monto=monto, tipo= 'Ingreso',tipoDeFactura= 'E',  observaciones=observaciones)
										facturaExpensa.save()	
										#Procedo a realizar los movimientos en las cajas 
										cajacons.montoActual = cajacons.montoActual + float(facturaExpensa.monto)
										cajacons.save()
										if seguir=='si': 
											context = {} 
											return render(request, "agregarFacturas.html", context)	 
										else:	
											context = {}
											return render(request, "accionExitosa.html", context)		
									else:#SI EXISTE LA Expensa; ERROR
										context = {}
										return render(request, "agregarFacturasErrorFactura.html", context)										
		else:
			context = {}
			return render(request, "agregarFacturas.html", context)	
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')	

#----------------------------------------------------------------ALERTAS-----------------------------------------------------------------------------				

def agregarAlerta(request):	#Funcion para mostrar los estadisticas en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			nombre = request.POST['nombre']
			fechaVencimiento = request.POST['vencimiento']
			descripcion = request.POST['descripcion']
			esMensual = request.POST['esMensual']
			resultado = 0
			if resultado == 0:
				alerta = Alerta.objects.create(nombre = nombre , fechaVencimiento = fechaVencimiento, descripcion = descripcion , esMensual = esMensual)
				alerta.save()
				return render_to_response('accionExitosa.html', context_instance=RequestContext(request))
			else:
					context = {}
					return render(request, "agregarAlerta.html", context)
					
		return render_to_response('agregarAlerta.html', context_instance=RequestContext(request))
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')	

def mostrarAlerta(request):#Muestro las alertas pero no agrego codigo porque solo es mostrar
	if request.user.is_authenticated():#Si el usuario esta identificado
		alertas	 = Alerta.objects.all().order_by('fechaVencimiento') #Las ordeno por fecha, asi te muestra las primeras que se venceran
		return render_to_response('mostrarAlerta.html', {'alertas':alertas}, context_instance=RequestContext(request))
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
	
def eliminarAlerta(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			resultado = 1
			valor = request.POST['valor']
			id = request.POST['id']
			resultado = 0
			if resultado == 0:
				validacionAlerta = Alerta.objects.filter(id = id)
				if validacionAlerta.exists()== True:
					alerta = Alerta.objects.get(id = id )
					if valor=='1':
						alerta.delete()
						context = {}
						return render(request, "accionExitosa.html", context)	
					elif valor=='2':
						context = {}
						return render(request, "eliminarAlerta.html", context)	
				else:
					context = {}
			return render(request, "eliminarAlertaError.html", context)
		else:
			context = {}
			return render(request, "eliminarAlerta.html", context)
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
	
def mostrarEstadisticas(request):	#Funcion para los MOVIMIENTOS TOTALES
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			tiempo = request.POST['tiempo'] #Tiempo a recorrer, 1 dia, 2mes, 3 periodo
			if tiempo == '1':
				dia = request.POST['dia']
			if tiempo == '2':
				mes = request.POST['mes']
			if tiempo == '3':
				fechaInicio = request.POST['fechaInicio']
				fechaCierre = request.POST['fechaCierre']
			caja = request.POST['caja'] #Para saber si sera de la Administracion o un Consorcio
			consorcio = request.POST['consorcio']
			
			#----------VARIABLES PARA UN DIA ESPECIFICO
			ingresosTotalesConsorcioDia = 0
			egresosTotalesConsorcioDia = 0
			ingresosTotalesAdministracionDia = 0
			egresosTotalesAdministracionDia = 0
			resumenDia = 0
			
			#------------------------------------------
			
			#----------VARIABLES PARA UN MES ESPECIFICO
			ingresosTotalesConsorcioMes = 0
			egresosTotalesConsorcioMes = 0
			ingresosTotalesAdministracionMes = 0
			egresosTotalesAdministracionMes = 0
			resumenMes = 0
			
			
			#------------------------------------------
			
			#----------VARIABLES PARA UN PERIODO ESPECIFICO
			ingresosTotalesConsorcioPeriodo = 0
			egresosTotalesConsorcioPeriodo = 0
			ingresosTotalesAdministracionPeriodo = 0
			egresosTotalesAdministracionPeriodo = 0
			resumenPeriodo = 0
			
			#------------------------------------------
			
			resultado = 0
			if resultado == 0:
				admin = Administracion.objects.get(id = 1)
				consorcioDato = None
				#-------------------------------------------------------
				if tiempo == '1': #Si elijo un dia especifico
					#----------------------------# # Si elijo la ADMINISTRACION
					if caja == '1':
						cajasAdministracion = CajaAdministracion.objects.all()
						facturasDiaEspecificoAdministracion = Factura.objects.all().filter( fechaPago=dia)
						for f in facturasDiaEspecificoAdministracion:
							for c in cajasAdministracion:
								if f.cajaAdministracion_id == c.id:
									if f.tipo == 'Ingreso':
										ingresosTotalesAdministracionDia = ingresosTotalesAdministracionDia + f.monto
									else:
										egresosTotalesAdministracionDia = egresosTotalesAdministracionDia +f.monto
						resumenDia = ingresosTotalesAdministracionDia - egresosTotalesAdministracionDia
					#----------------------------#Si la Caja elegida es el CONSORCIO
					else:
						verificacionConsorcioDia = Consorcio.objects.filter(id = consorcio)
						if verificacionConsorcioDia.exists() == False:	#Si no existe el consorcio, la creo
							context = {}
							return render(request, "agregarConsorcio.html", context)
						else:#Si existe el consorcio, prosigo
							#Traigo todas las cajas del consorcio donde puedo sumar datos y las facturas	
							consorcioDato = Consorcio.objects.get(id = consorcio)
							facturasDiaEspecificoConsorcio = Factura.objects.all().filter( fechaPago=dia)
							cajasConsorcioDia = CajaConsorcio.objects.all().filter(consorcio_id = consorcio)
							for f in facturasDiaEspecificoConsorcio:
								for c in cajasConsorcioDia:
									if c.id == f.cajaConsorcio_id :
										if f.tipo == 'Ingreso':
											ingresosTotalesConsorcioDia = ingresosTotalesConsorcioDia + f.monto
										else:
											egresosTotalesConsorcioDia = egresosTotalesConsorcioDia +f.monto
							resumenDia = ingresosTotalesConsorcioDia - egresosTotalesConsorcioDia
					
					return render_to_response('mostrarEstadisticas1.html',{'tiempo':tiempo, 'caja':caja,
					'resumenDia':resumenDia,
					'ingresosTotalesAdministracionDia':ingresosTotalesAdministracionDia,
					'egresosTotalesAdministracionDia':egresosTotalesAdministracionDia,
					'ingresosTotalesConsorcioDia': ingresosTotalesConsorcioDia,
					'egresosTotalesConsorcioDia': egresosTotalesConsorcioDia,
					'administracion':admin, 'consorcioDato': consorcioDato,
					'dia':dia 
					} ,context_instance=RequestContext(request))		

					
					#---------------------------------------------------	
					
					
				if tiempo == '2':# Si elijo un mes especifico
					#LE AGREGO UN 0 Al string para poder compararlo
					mes = int(mes)
					mes = mes+1 #SUMO UNO PORQUE LA INTERFAZ DEVUELVE DESDE CERO
					if mes <10:
						mes = str(mes)
						mes = '0'+ mes
					#----------------------------# # Si elijo la ADMINISTRACION	
					if caja == '1': # Si elijo la ADMINISTRACION
						cajasAdministracion = CajaAdministracion.objects.all()
						facturasMesEspecificoAdministracion = Factura.objects.all()
						for f in facturasMesEspecificoAdministracion:
							for c in cajasAdministracion:
								fechaString= str(f.fechaPago)
								x = fechaString[5] + fechaString[6]
								if f.cajaAdministracion_id == c.id:
									if x == str(mes):
										if f.tipo == 'Ingreso':
											ingresosTotalesAdministracionMes = ingresosTotalesAdministracionMes + f.monto
										else:
											egresosTotalesAdministracionMes = egresosTotalesAdministracionMes +f.monto
						resumenMes = ingresosTotalesAdministracionMes - egresosTotalesAdministracionMes
					#----------------------------#Si la Caja elegida es el CONSORCIO
					else:#Si la Caja elegida es el CONSORCIO
						verificacionConsorcioMes = Consorcio.objects.filter(id =consorcio)
						if verificacionConsorcioMes.exists() == False:	#Si no existe el consorcio, lo creo
							context = {}
							return render(request, "agregarConsorcio.html", context)
						else:#Si existe el consorcio, prosigo
							consorcioDato = Consorcio.objects.get(id = consorcio)
							facturasMesEspecificoConsorcio = Factura.objects.all()
							cajasConsorcioMes = CajaConsorcio.objects.all().filter(consorcio_id = consorcio)
							for c in cajasConsorcioMes:
								for f in facturasMesEspecificoConsorcio:
									fechaString= str(f.fechaPago)
									x = fechaString[5] + fechaString[6]
									if c.id == f.cajaConsorcio_id :
										if x == str(mes):
											if f.tipo == 'Ingreso' :
												ingresosTotalesConsorcioMes = ingresosTotalesConsorcioMes + f.monto
											else:
												egresosTotalesConsorcioMes = egresosTotalesConsorcioMes +f.monto
							resumenMes = ingresosTotalesConsorcioMes - egresosTotalesConsorcioMes
				return render_to_response('mostrarEstadisticas1.html',{'tiempo':tiempo, 'caja':caja,'ingresosTotalesAdministracionMes':ingresosTotalesAdministracionMes,
					'mes':mes,'egresosTotalesAdministracionMes':egresosTotalesAdministracionMes,
					'ingresosTotalesConsorcioMes': ingresosTotalesConsorcioMes,
					'egresosTotalesConsorcioMes': egresosTotalesConsorcioMes,
					'administracion':admin, 'consorcioDato': consorcioDato,'resumenMes':resumenMes
					
					} ,context_instance=RequestContext(request))	
					
					
				#----------------------------------------------------
				
				if tiempo == '3':#Si elijo un periodo de tiempo
					if fechaInicio >= fechaCierre: #DEBERIA APARECER ALGO QUE MUESTRE ERROR
						return render_to_response('mostrarEstadisticasEfectivo.html',context_instance=RequestContext(request))
					#---------------------------------
					#----------------------------# # Si elijo la ADMINISTRACION
					if caja == '1': # Si elijo la ADMINISTRACION
						cajasAdministracion = CajaAdministracion.objects.all()
						facturasPeriodoAdministracion = Factura.objects.all()
						for f in facturasPeriodoAdministracion:
							for c in cajasAdministracion:
								if f.cajaAdministracion_id == c.id:
									if str(f.fechaPago) >= fechaInicio and str(f.fechaPago) <= fechaCierre:
										if f.tipo == 'Ingreso':
											ingresosTotalesAdministracionPeriodo = ingresosTotalesAdministracionPeriodo + f.monto
										else:
											egresosTotalesAdministracionPeriodo = egresosTotalesAdministracionPeriodo +f.monto
						resumenPeriodo = ingresosTotalesAdministracionPeriodo - egresosTotalesAdministracionPeriodo					
					#----------------------------#Si la Caja elegida es el CONSORCIO
					else:#Si la Caja elegida es el CONSORCIO
						verificacionConsorcioPeriodo = Consorcio.objects.filter(id =consorcio)
						if verificacionConsorcioPeriodo.exists() == False:	#Si no existe el consorcio, la creo
							context = {}
							return render(request, "agregarConsorcio.html", context)
						else:#Si existe el consorcio, prosigo
							consorcioDato = Consorcio.objects.get(id = consorcio)
							facturasPeriodoEspecificoConsorcio = Factura.objects.all()
							cajasConsorcioPeriodo = CajaConsorcio.objects.all().filter(consorcio_id = consorcio)
							for c in cajasConsorcioPeriodo:
								for f in facturasPeriodoEspecificoConsorcio:
									if c.id == f.cajaConsorcio_id :
										if str(f.fechaPago) >= fechaInicio and str(f.fechaPago) <= fechaCierre:
											if f.tipo == 'Ingreso' :
												ingresosTotalesConsorcioPeriodo = ingresosTotalesConsorcioPeriodo + f.monto
											else:
												egresosTotalesConsorcioPeriodo = egresosTotalesConsorcioPeriodo +f.monto
							resumenPeriodo = ingresosTotalesConsorcioPeriodo - egresosTotalesConsorcioPeriodo
				return render_to_response('mostrarEstadisticas1.html',{ 'tiempo':tiempo, 'caja':caja,
					'ingresosTotalesAdministracionPeriodo':ingresosTotalesAdministracionPeriodo,
					'egresosTotalesAdministracionPeriodo':egresosTotalesAdministracionPeriodo,
					'ingresosTotalesConsorcioPeriodo': ingresosTotalesConsorcioPeriodo,
					'egresosTotalesConsorcioPeriodo': egresosTotalesConsorcioPeriodo,
					'administracion':admin, 'consorcioDato': consorcioDato,'resumenPeriodo':resumenPeriodo,
					'fechaInicio':fechaInicio, 'fechaCierre': fechaCierre
					} ,context_instance=RequestContext(request))	

				
		return render_to_response('mostrarEstadisticas.html',context_instance=RequestContext(request))	
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
		 
def mostrarEstadisticasEfectivo(request):	#Funcion para los MOVIMIENTOS de la cuenta EFECTIVO
	if request.user.is_authenticated():#Si el usuario esta identificado
		if request.method == "POST":
			tiempo = request.POST['tiempo'] #Tiempo a recorrer, 1 dia, 2mes, 3 periodo
			if tiempo == '1':
				dia = request.POST['dia']
			if tiempo == '2':
				mes = request.POST['mes']
			if tiempo == '3':
				fechaInicio = request.POST['fechaInicio']
				fechaCierre = request.POST['fechaCierre']
			caja = request.POST['caja'] #Para saber si sera de la Administracion o un Consorcio
			consorcio = request.POST['consorcio']
			
			#----------VARIABLES PARA UN DIA ESPECIFICO
			ingresosTotalesConsorcioDia = 0
			egresosTotalesConsorcioDia = 0
			ingresosTotalesAdministracionDia = 0
			egresosTotalesAdministracionDia = 0
			resumenDia = 0
			
			#------------------------------------------
			
			#----------VARIABLES PARA UN MES ESPECIFICO
			ingresosTotalesConsorcioMes = 0
			egresosTotalesConsorcioMes = 0
			ingresosTotalesAdministracionMes = 0
			egresosTotalesAdministracionMes = 0
			resumenMes = 0
			
			#------------------------------------------
			
			#----------VARIABLES PARA UN PERIODO ESPECIFICO
			ingresosTotalesConsorcioPeriodo = 0
			egresosTotalesConsorcioPeriodo = 0
			ingresosTotalesAdministracionPeriodo = 0
			egresosTotalesAdministracionPeriodo = 0
			resumenPeriodo = 0
			
			#------------------------------------------
			
			resultado = 0
			if resultado == 0:
				admin = Administracion.objects.get(id = 1)
				consorcioDato = None
				#-------------------------------------------------------
				if tiempo == '1': #Si elijo un dia especifico
					#----------------------------# # Si elijo la ADMINISTRACION
					if caja == '1':
						cajasAdministracion = CajaAdministracion.objects.all().filter(tipoDeCaja = 3)
						facturasDiaEspecificoAdministracion = Factura.objects.all().filter( fechaPago=dia)
						for f in facturasDiaEspecificoAdministracion:
							for c in cajasAdministracion:
								if f.cajaAdministracion_id == c.id:
									if f.tipo == 'Ingreso':
										ingresosTotalesAdministracionDia = ingresosTotalesAdministracionDia + f.monto
									else:
										egresosTotalesAdministracionDia = egresosTotalesAdministracionDia +f.monto
						resumenDia = ingresosTotalesAdministracionDia - egresosTotalesAdministracionDia
					#----------------------------#Si la Caja elegida es el CONSORCIO
					else:
						verificacionConsorcioDia = Consorcio.objects.filter(id = consorcio)
						if verificacionConsorcioDia.exists() == False:	#Si no existe el consorcio, la creo
							context = {}
							return render(request, "agregarConsorcio.html", context)
						else:#Si existe el consorcio, prosigo
							#Traigo todas las cajas del consorcio donde puedo sumar datos y las facturas	
							consorcioDato = Consorcio.objects.get(id = consorcio)
							facturasDiaEspecificoConsorcio = Factura.objects.all().filter( fechaPago=dia)
							cajasConsorcioDia = CajaConsorcio.objects.all().filter(consorcio_id = consorcio, tipoDeCaja = '3')
							for f in facturasDiaEspecificoConsorcio:
								for c in cajasConsorcioDia:
									if c.id == f.cajaConsorcio_id :
										if f.tipo == 'Ingreso':
											ingresosTotalesConsorcioDia = ingresosTotalesConsorcioDia + f.monto
										else:
											egresosTotalesConsorcioDia = egresosTotalesConsorcioDia +f.monto
							resumenDia = ingresosTotalesConsorcioDia - egresosTotalesConsorcioDia
					
					return render_to_response('mostrarEstadisticas1.html',{'tiempo':tiempo, 'caja':caja,
					'resumenDia':resumenDia,
					'ingresosTotalesAdministracionDia':ingresosTotalesAdministracionDia,
					'egresosTotalesAdministracionDia':egresosTotalesAdministracionDia,
					'ingresosTotalesConsorcioDia': ingresosTotalesConsorcioDia,
					'egresosTotalesConsorcioDia': egresosTotalesConsorcioDia,
					'administracion':admin, 'consorcioDato': consorcioDato,
					'dia':dia 
					} ,context_instance=RequestContext(request))		

					
					#---------------------------------------------------	
					
					
				if tiempo == '2':# Si elijo un mes especifico
					#LE AGREGO UN 0 Al string para poder compararlo
					mes = int(mes)
					mes = mes+1 #SUMO UNO PORQUE LA INTERFAZ DEVUELVE DESDE CERO
					if mes <10:
						mes = str(mes)
						mes = '0'+ mes
					#----------------------------# # Si elijo la ADMINISTRACION	
					if caja == '1': # Si elijo la ADMINISTRACION
						cajasAdministracion = CajaAdministracion.objects.all().filter(tipoDeCaja = '3')
						facturasMesEspecificoAdministracion = Factura.objects.all()
						for f in facturasMesEspecificoAdministracion:
							for c in cajasAdministracion:
								fechaString= str(f.fechaPago)
								x = fechaString[5] + fechaString[6]
								if f.cajaAdministracion_id == c.id:
									if x == str(mes):
										if f.tipo == 'Ingreso':
											ingresosTotalesAdministracionMes = ingresosTotalesAdministracionMes + f.monto
										else:
											egresosTotalesAdministracionMes = egresosTotalesAdministracionMes +f.monto
						resumenMes = ingresosTotalesAdministracionMes - egresosTotalesAdministracionMes
					#----------------------------#Si la Caja elegida es el CONSORCIO
					else:#Si la Caja elegida es el CONSORCIO
						verificacionConsorcioMes = Consorcio.objects.filter(id =consorcio)
						if verificacionConsorcioMes.exists() == False:	#Si no existe el consorcio, lo creo
							context = {}
							return render(request, "agregarConsorcio.html", context)
						else:#Si existe el consorcio, prosigo
							consorcioDato = Consorcio.objects.get(id = consorcio)
							facturasMesEspecificoConsorcio = Factura.objects.all()
							cajasConsorcioMes = CajaConsorcio.objects.all().filter(consorcio_id = consorcio, tipoDeCaja = '3')
							for c in cajasConsorcioMes:
								for f in facturasMesEspecificoConsorcio:
									fechaString= str(f.fechaPago)
									x = fechaString[5] + fechaString[6]
									if c.id == f.cajaConsorcio_id :
										if x == str(mes):
											if f.tipo == 'Ingreso' :
												ingresosTotalesConsorcioMes = ingresosTotalesConsorcioMes + f.monto
											else:
												egresosTotalesConsorcioMes = egresosTotalesConsorcioMes +f.monto
							resumenMes = ingresosTotalesConsorcioMes - egresosTotalesConsorcioMes
				return render_to_response('mostrarEstadisticas1.html',{'tiempo':tiempo, 'caja':caja,'ingresosTotalesAdministracionMes':ingresosTotalesAdministracionMes,
					'mes':mes,'egresosTotalesAdministracionMes':egresosTotalesAdministracionMes,
					'ingresosTotalesConsorcioMes': ingresosTotalesConsorcioMes,
					'egresosTotalesConsorcioMes': egresosTotalesConsorcioMes,
					'administracion':admin, 'consorcioDato': consorcioDato,'resumenMes':resumenMes
					
					} ,context_instance=RequestContext(request))	
					
					
				#----------------------------------------------------
				
				if tiempo == '3':#Si elijo un periodo de tiempo
					if fechaInicio >= fechaCierre: #DEBERIA APARECER ALGO QUE MUESTRE ERROR
						return render_to_response('mostrarEstadisticasEfectivo.html',context_instance=RequestContext(request))
					#---------------------------------
					#----------------------------# # Si elijo la ADMINISTRACION
					if caja == '1': # Si elijo la ADMINISTRACION
						cajasAdministracion = CajaAdministracion.objects.all().filter(tipoDeCaja = '3')
						facturasPeriodoAdministracion = Factura.objects.all()
						for f in facturasPeriodoAdministracion:
							for c in cajasAdministracion:
								if f.cajaAdministracion_id == c.id:
									if str(f.fechaPago) >= fechaInicio and str(f.fechaPago) <= fechaCierre:
										if f.tipo == 'Ingreso':
											ingresosTotalesAdministracionPeriodo = ingresosTotalesAdministracionPeriodo + f.monto
										else:
											egresosTotalesAdministracionPeriodo = egresosTotalesAdministracionPeriodo +f.monto
						resumenPeriodo = ingresosTotalesAdministracionPeriodo - egresosTotalesAdministracionPeriodo					
					#----------------------------#Si la Caja elegida es el CONSORCIO
					else:#Si la Caja elegida es el CONSORCIO
						verificacionConsorcioPeriodo = Consorcio.objects.filter(id =consorcio)
						if verificacionConsorcioPeriodo.exists() == False:	#Si no existe el consorcio, la creo
							context = {}
							return render(request, "agregarConsorcio.html", context)
						else:#Si existe el consorcio, prosigo
							consorcioDato = Consorcio.objects.get(id = consorcio)
							facturasPeriodoEspecificoConsorcio = Factura.objects.all()
							cajasConsorcioPeriodo = CajaConsorcio.objects.all().filter(consorcio_id = consorcio, tipoDeCaja = '3')
							for c in cajasConsorcioPeriodo:
								for f in facturasPeriodoEspecificoConsorcio:
									if c.id == f.cajaConsorcio_id :
										if str(f.fechaPago) >= fechaInicio and str(f.fechaPago) <= fechaCierre:
											if f.tipo == 'Ingreso' :
												ingresosTotalesConsorcioPeriodo = ingresosTotalesConsorcioPeriodo + f.monto
											else:
												egresosTotalesConsorcioPeriodo = egresosTotalesConsorcioPeriodo +f.monto
							resumenPeriodo = ingresosTotalesConsorcioPeriodo - egresosTotalesConsorcioPeriodo
				return render_to_response('mostrarEstadisticas1.html',{ 'tiempo':tiempo, 'caja':caja,
					'ingresosTotalesAdministracionPeriodo':ingresosTotalesAdministracionPeriodo,
					'egresosTotalesAdministracionPeriodo':egresosTotalesAdministracionPeriodo,
					'ingresosTotalesConsorcioPeriodo': ingresosTotalesConsorcioPeriodo,
					'egresosTotalesConsorcioPeriodo': egresosTotalesConsorcioPeriodo,
					'administracion':admin, 'consorcioDato': consorcioDato,'resumenPeriodo':resumenPeriodo,
					'fechaInicio':fechaInicio, 'fechaCierre': fechaCierre
					} ,context_instance=RequestContext(request))	

				
		return render_to_response('mostrarEstadisticasEfectivo.html',context_instance=RequestContext(request))	
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
	
def arqueoCajas(request):
	if request.user.is_authenticated():#Si el usuario esta identificado
		cajasAdministracion = CajaAdministracion.objects.all().order_by( 'tipoDeCaja')
		cajasConsorcio = CajaConsorcio.objects.all().order_by('consorcio_id', 'tipoDeCaja')
		consorcios = Consorcio.objects.all()
		
		return render_to_response('arqueoCajas.html', {'cajasAdministracion':cajasAdministracion,
		'cajasConsorcio':cajasConsorcio,
		'consorcios':consorcios}, context_instance=RequestContext(request))
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')

	
def consorcio(request):	#Funcion para mostrar los consorcios en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado
		return render_to_response('consorcio.html', context_instance=RequestContext(request))	
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
		 
def ejemplo(request):	#Funcion para mostrar la interfaz base
	if request.user.is_authenticated():#Si el usuario esta identificado
		return render_to_response('ejemplo.html', context_instance=RequestContext(request))
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')
		 
def reclamo(request):	#Funcion para mostrar los consorcios en la pagina
	if request.user.is_authenticated():#Si el usuario esta identificado
		return render_to_response('reclamo.html', context_instance=RequestContext(request))	
	else:
		 return redirect('/AdminConsorcios/usuario/iniciarsesion/')

	
@login_required(login_url='/ingresar')
def privado(request):
    usuario = request.user
    return render_to_response('privado.html', {'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')
	
