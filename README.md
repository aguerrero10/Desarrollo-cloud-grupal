# Desarrollo de Soluciones Cloud 2023-1

Repositorio del proyecto de Desarrollo de Soluciones Cloud 2023-1, entrega final del proyecto.

## Integrantes del grupo
Grupo de trabajo: 6
* Javier Alejandro Gómez
* Alejandra Guerrero
* Diego Alejandro Peña
* Juan Ignacio Arbeláez

## Video sustentación
El video se encuentra en el siguiente enlace: [DSC-EntregaFinal](https://uniandes-my.sharepoint.com/:v:/r/personal/a_guerrero10_uniandes_edu_co/Documents/Grabaciones/DSC-EntregaFinal.mp4?csf=1&web=1&e=uXuKEF)

## Código
- [WebServer](WebServer/flaskr): código usado para el despliegue del Servidor Web en Cloud Run. Permite crear usuarios, iniciar sesión, solicitar y consultar tareas de compresión, descargar archivos, entre otros.
- [Worker](Worker): código desplegado en Cloud Run para la compresión de los archivos y notificación por email del éxito de la tarea de compresión.
- [Test](Test): elementos usados para la ejecución de los escenarios de prueba 

## Documentación
El documento [Entrega 5 - Arquitectura, conclusiones y consideraciones.pdf](Documentacion/Entrega%205%20-%20Arquitectura%2C%20conclusiones%20y%20consideraciones.pdf), el cual contiene el diseño, particularidades y conclusiones del proyecto, se encuentra en la carpeta Documentación.

Los endpoints desarrollados se encuentran documentados a través de la aplicación Postman.
Podrá encontrar el documento en el siguiente vínculo:
https://documenter.getpostman.com/view/13843294/2s93CPrY2y