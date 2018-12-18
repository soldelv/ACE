from django.db import models

# Create your models here.

#class Usuario(models.Model):
#	nombre=models.CharField(max_length=30)	
#	apellido=models.CharField(max_length=30)
#	usuario=models.CharField(max_length=30)
#	clave=models.CharField(max_length=30)
#	confclave=models.CharField(max_length=30)
	
class Administracion(models.Model):
    razonSocial = models.CharField(max_length=50)

class Consorcio(models.Model):
	administracion = models.ForeignKey(Administracion,null=True, on_delete= models.CASCADE)
	razonSocial = models.CharField(max_length=50)
	direccion = models.CharField(max_length=50)
	cp = models.CharField(max_length=10)
	localidad = models.CharField(max_length=50)
	cuit = models.CharField(max_length=15)
	cantidadCocheras = models.IntegerField()
	cantidadUnidadesFuncionales = models.IntegerField()
	actividadEconomica = models.CharField(max_length=50)
	administrador = models.CharField(max_length = 30) #cambio
	suterh = models.CharField(max_length = 30)
	clavesuterh = models.CharField(max_length = 30)#agregada
	responsabilidadIVA = models.CharField(max_length = 30)
	cantidadAsensores = models.IntegerField()
	cantidadCalderas = models.IntegerField(default = 0)
	fechaContratoSocial = models.DateField(blank=True)#cambio
	inicioAdministracion = models.DateField(blank=True)#cambio
	esBaja = models.BooleanField(default=False)
	cantidadTermotanques = models.IntegerField()#agregada
	instalacionesFijas = models.BooleanField(default=False)#agregada
	agencia = models.IntegerField()#agregada
	categoria = models.CharField(max_length=50)#agregada
	numero = models.IntegerField()#agregada
		
#class Servicio(models.Model):
#   nombre = models.CharField(max_length=50)
#    descripcion = models.CharField(max_length=50)
#    consorcio = models.ManyToManyField(Consorcio, blank=True)
	
class Propietario(models.Model):
	nombre = models.CharField(max_length=20)
	apellido = models.CharField(max_length=20)
	dni = models.CharField(max_length=10)
	email = models.EmailField(max_length=50)
	telFijo = models.CharField(max_length=10)
	celular = models.CharField(max_length=20)
	direccion = models.CharField(max_length=50)
	cp = models.CharField(max_length=10)
	localidad = models.CharField(max_length=50)
	observaciones = models.TextField()#agregada

class Inquilino(models.Model):
	nombre = models.CharField(max_length=20)
	apellido = models.CharField(max_length=20)
	dni = models.CharField(max_length=10)
	email = models.EmailField(max_length=50)
	telFijo = models.CharField(max_length=10)
	celular = models.CharField(max_length=20)
	observaciones = models.TextField()#agregada

class UnidadFuncional(models.Model):
    consorcio = models.ForeignKey(Consorcio, null=True, blank=True, on_delete= models.CASCADE)
    propietario = models.ForeignKey(Propietario, null=True, blank=True, on_delete= models.CASCADE)
    inquilino = models.ForeignKey(Inquilino, null=True, blank=True, on_delete= models.CASCADE)
    alquilado = models.BooleanField(default=False)
    unidadFuncional = models.IntegerField()#cambio
    pisoDepartamento = models.CharField(max_length=10)#cambio
	
ESTADOS = ((1, "Iniciado"),(2, "Pendiente"),(3, "Terminado"))
class Reclamo(models.Model):
	unidadFuncional = models.ForeignKey(UnidadFuncional,null=True, blank=True, on_delete= models.CASCADE)
	consorcio = models.ForeignKey(Consorcio,null=True, blank=True, on_delete= models.CASCADE)
	fecha = models.DateField(blank=True)
	ubicacion = models.CharField(max_length=50)
	descripcion = models.TextField()#cambio
	estado = models.CharField(max_length=20)
	esBaja = models.BooleanField(default=False)
	
class Empleado(models.Model):
	consorcio = models.ForeignKey(Consorcio, null=True, blank=True, on_delete=models.CASCADE)
	admin = models.ForeignKey(Administracion, null=True, blank=True, on_delete=models.CASCADE)
	nombre = models.CharField(max_length=15)
	apellido = models.CharField(max_length=20)
	dni = models.CharField(max_length=10)
	cuil = models.CharField(max_length=15)
	nacionalidad = models.CharField(max_length=15)
	email = models.EmailField(max_length=50)
	telFijo = models.CharField(max_length=10)
	celular = models.CharField(max_length=20)
	direccion = models.CharField(max_length=50)
	cp = models.CharField(max_length=10)
	localidad = models.CharField(max_length=50)
	estadoCivil = models.CharField(max_length=50)#agregada
	estudios = models.CharField(max_length=50)#agregada
	funcion = models.CharField(max_length=50)#agregada
	categoriaFuncion = models.CharField(max_length=50)#agregada
	fechaNacimiento = models.DateField(blank=True)#agregada
	ingreso = models.DateField(blank=True)#agregada
	horarioSemanalInicio = models.TimeField(blank=True, null=True)#agregada
	horarioSemanalFin = models.TimeField(blank=True, null=True)#agregada
	horarioSemanalAdicionalInicio = models.TimeField(blank=True, null=True)#agregada
	horarioSemanalAdicionalFin = models.TimeField(blank=True, null=True)#agregada
	horarioSabadoInicio = models.TimeField(blank=True, null=True)#agregada
	horarioSabadoFin = models.TimeField(blank=True, null=True)#agregada
	horarioSabadoAdicionalInicio = models.TimeField(blank=True, null=True)#agregada
	horarioSabadoAdicionalFin = models.TimeField(blank=True, null=True)#agregada
	horarioDomingoInicio = models.TimeField(blank=True, null=True)#agregada
	horarioDomingoFin = models.TimeField(blank=True, null=True)#agregada
	horarioDomingoAdicionalInicio = models.TimeField(blank=True, null=True)#agregada
	horarioDomingoAdicionalFin = models.TimeField(blank=True, null=True)#agregada
	horarioFeriadoInicio = models.TimeField(blank=True, null=True)#agregada
	horarioFeriadoFin = models.TimeField(blank=True, null=True)#agregada
	horarioFeriadoAdicionalInicio = models.TimeField(blank=True, null=True)#agregada
	horarioFeriadoAdicionalFin = models.TimeField(blank=True, null=True)#agregada
	observaciones = models.TextField()#agregada
	

TIPOCAJA = ((1, "Efectiva"),(2, "Bancaria"),(3, "Cheque"))
class CajaConsorcio(models.Model):
	consorcio = models.ForeignKey(Consorcio, null=True, blank=True, on_delete= models.CASCADE)
	tipoDeCaja = models.IntegerField()#cambio
	montoActual = models.FloatField(default=0)
	banco = models.CharField(max_length=50)#agregada
	nroCuenta = models.CharField(max_length=30)#agregada
	moneda = models.CharField(max_length=20)#agregada

class CajaAdministracion(models.Model):
	administracion = models.ForeignKey(Administracion, null=True, blank=True, on_delete= models.CASCADE)
	tipoDeCaja = models.IntegerField()#cambio
	montoActual = models.FloatField(default=0)
	banco = models.CharField(max_length=50)#agregada
	nroCuenta = models.CharField(max_length=30)#agregada
	moneda = models.CharField(max_length=20)#agregada
    
#Modificado, Ahora es una unica factura

TIPO = ((1, "Ingreso"),(2, "Egreso"))
class Factura(models.Model):
	cajaConsorcio = models.ForeignKey(CajaConsorcio, null=True, blank=True, on_delete= models.CASCADE)
	cajaAdministracion = models.ForeignKey(CajaAdministracion, null=True, blank=True, on_delete= models.CASCADE)
	unidadFuncional = models.IntegerField(null=True)#agregada
	pisoDepartamento = models.CharField(max_length=10)#agregada
	numero = models.CharField(max_length=15)
	factura = models.CharField(max_length=25)
	#servicio = models.CharField(max_length=50)
	#gasto = models.CharField(max_length=50)
	#abono = models.CharField(max_length=50)
	#fechaVencimiento = models.DateField(blank=True)
	fechaPago = models.DateField(blank=True)
	monto = models.FloatField(default=0)
	tipo = models.CharField(max_length=10)#modificado
	esBaja = models.BooleanField(default=False)
	fechaEmision = models.DateField(blank=True, null=True)#agregada 
	tipoDeFactura = models.CharField(max_length=20)#agregada
	observaciones = models.TextField()#agregada
	#proveedor = models.CharField(max_length=50)#agregada

#Ultimo Agregado	
class Reporte(models.Model):
	fecha = models.DateField(blank=True)
	ingreso = models.FloatField(default=0)
	egreso = models.FloatField(default=0)
	montoInicial = models.FloatField(default=0)
	montoActual = models.FloatField(default=0)

class Alerta(models.Model):
	nombre = models.CharField(max_length=45)#agregada
	fechaVencimiento = models.DateField(blank=True)#agregada
	descripcion = models.TextField()#agregada
	esMensual = models.BooleanField(default=False)#agregada
	
#class Abono(models.Model):
#	propietario = models.ForeignKey(Propietario, null=True, blank=True, on_delete= models.CASCADE)
#	nombre = models.CharField(max_length=30)
#	descripcion = models.CharField(max_length=50)
#	consorcio = models.ManyToManyField(Consorcio, blank=True)

#class Gasto(models.Model):
#	nombre = models.CharField(max_length=30)
#	descripcion = models.CharField(max_length=50)
#	consorcio = models.ManyToManyField(Consorcio, blank=True)
	
		
		

