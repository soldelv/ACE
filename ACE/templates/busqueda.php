<?php

// Primero definimos la conexión a la base de datos, para que se fácil cambiar los parámetros si procede.
define('HOST_DB', 'localhost');  //Nombre del host, nomalmente localhost
define('USER_DB', 'root');       //Usuario de la bbdd
define('PASS_DB', '');           //Contraseña de la bbdd
define('NAME_DB', 'consorcios'); //Nombre de la bbdd


// Definimos la conexión (versión PHP 7)
function conectar(){
    global $conexion;  //Definición global para poder utilizar en todo el contexto
    $conexion = mysqli_connect(HOST_DB, USER_DB, PASS_DB, NAME_DB)
    or die ('NO SE HA PODIDO CONECTAR AL MOTOR DE LA BASE DE DATOS');
    mysqli_select_db($conexion, NAME_DB)
    or die ('NO SE ENCUENTRA LA BASE DE DATOS ' . NAME_DB);
}
function desconectar(){
    global $conexion;
    mysqli_close($conexion);
}


function opciones() {
	global $conexion;
      //Variable que contendrá el resultado de la búsqueda
	  $texto = '';

	  conectar();
      mysqli_set_charset($conexion, 'utf8');  // para indicar a la bbdd que vamos a mostrar la info en utf8
	  
	  //Contulta para recoger la información de todas las provincias
	  $sql = "SELECT * FROM consorcio ORDER BY razonSocial";
	  
	  $resultado = mysqli_query($conexion, $sql); //Ejecución de la consulta
      //Si hay resultados...
	  if (mysqli_num_rows($resultado) > 0){ 

		 while($fila = mysqli_fetch_assoc($resultado)){ 
		      // se recoge la información según la vamos a pasar a la variable de javascript
              $texto .= '"' . $fila['Consorcio'] . '",';
			 }
	  
	  }else{
			   $texto = "NO HAY RESULTADOS EN LA BBDD";	
	  }
	  // Después de trabajar con la bbdd, cerramos la conexión (por seguridad, no hay que dejar conexiones abiertas)
	  mysqli_close($conexion);
      
	  return $texto;
}
?>
